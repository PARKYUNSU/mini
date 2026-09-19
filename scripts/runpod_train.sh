#!/bin/bash
# yunsur LoRA — RunPod Pod 시작 명령(Docker Command). clone → 설치 → 학습 → HF Hub private 업로드 → Pod 자동 종료.
#
# Pod 설정 (RunPod MCP / 콘솔):
#   이미지    runpod/pytorch:2.4.0-py3.11-cuda12.4.1  (v4 와 동일; torch 는 아래에서 2.5+ cu124 로 올림)
#   GPU       L40S 48GB · 볼륨 50GB (/workspace) — v4 때 20GB 로 부족했음
#   시작 명령 bash -c "curl -fsSL https://raw.githubusercontent.com/PARKYUNSU/mini/main/scripts/runpod_train.sh | bash"
#            (레포가 private 이면 GH_TOKEN 이 필요하므로 아래 방식으로: )
#            bash -c "git clone https://\${GH_TOKEN}@github.com/PARKYUNSU/mini.git /workspace/mini && bash /workspace/mini/scripts/runpod_train.sh"
#   환경변수  HF_TOKEN = {{ RUNPOD_SECRET_HF_TOKEN }}   ← RunPod Secret 참조. 값은 어디에도 적지 않는다.
#            HF_REPO  = <hf_user>/yunsur_v5_lora        (private 모델 레포, 없으면 스크립트가 생성)
#            VERSION  = v5
#            GH_TOKEN = {{ RUNPOD_SECRET_GH_TOKEN }}    (레포가 private 일 때만)
#            GIT_REF  = main                            (선택: 태그·브랜치·커밋)
#            KEEP_POD = 1                               (선택: 디버깅용, 끝나도 Pod 안 끔)
#
# 결과 확인 (맥미니):
#   huggingface-cli download "$HF_REPO" --local-dir "/Volumes/T7 Shield/yunsur_v5_hub"   → adapter/, train_log.json, train_stats.json
#   로그 전체는 HF 레포 runpod_train.log 에도 올라간다 (Pod 이 종료돼도 남음).
set -uo pipefail

VERSION="${VERSION:-v5}"
GIT_REF="${GIT_REF:-main}"
REPO_DIR="${REPO_DIR:-/workspace/mini}"
REPO_HTTPS="https://github.com/PARKYUNSU/mini.git"
LOG="/workspace/runpod_train_${VERSION}.log"
mkdir -p /workspace
exec > >(tee -a "$LOG") 2>&1

step() { echo; echo "===== [$(date '+%H:%M:%S')] $* ====="; }
finish() {
  local rc=$1
  step "종료 처리 (rc=$rc)"
  # 로그를 HF 레포에 올려 Pod 종료 후에도 남긴다 (토큰·레포 있을 때만)
  if [[ -n "${HF_TOKEN:-}" && -n "${HF_REPO:-}" ]]; then
    python - <<PY || true
import os
from huggingface_hub import HfApi
api = HfApi()
api.create_repo(os.environ["HF_REPO"], repo_type="model", private=True, exist_ok=True)
api.upload_file(path_or_fileobj="$LOG", path_in_repo="runpod_train.log", repo_id=os.environ["HF_REPO"], repo_type="model")
print("로그 업로드 완료")
PY
  fi
  if [[ "${KEEP_POD:-0}" == "1" ]]; then
    echo "KEEP_POD=1 — Pod 유지"; exit "$rc"
  fi
  if [[ -n "${RUNPOD_POD_ID:-}" ]] && command -v runpodctl >/dev/null; then
    echo "Pod 종료: $RUNPOD_POD_ID"
    runpodctl remove pod "$RUNPOD_POD_ID" || runpodctl stop pod "$RUNPOD_POD_ID" || echo "⚠️ 자동 종료 실패 — 콘솔에서 직접 끌 것"
  else
    echo "⚠️ RUNPOD_POD_ID/runpodctl 없음 — 자동 종료 생략"
  fi
  exit "$rc"
}

step "0. 사전 확인 — VERSION=$VERSION GIT_REF=$GIT_REF"
[[ -n "${HF_TOKEN:-}" ]] || echo "⚠️ HF_TOKEN 없음 — 학습은 하지만 업로드 못 함 (RunPod Secret 확인)"
[[ -n "${HF_REPO:-}" ]]  || echo "⚠️ HF_REPO 없음 — 업로드 생략됨"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
df -h /workspace | tail -1

step "1. 레포"
if [[ ! -d "$REPO_DIR/.git" ]]; then
  if [[ -n "${GH_TOKEN:-}" ]]; then
    git clone --quiet "https://${GH_TOKEN}@github.com/PARKYUNSU/mini.git" "$REPO_DIR" || finish 10
  else
    git clone --quiet "$REPO_HTTPS" "$REPO_DIR" || finish 10
  fi
fi
cd "$REPO_DIR" || finish 10
git fetch --quiet origin "$GIT_REF" && git checkout --quiet FETCH_HEAD || finish 10
echo "commit: $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
DATA="finetune_datasets/${VERSION}/train_data_${VERSION}.jsonl"
[[ -f "$DATA" ]] || { echo "❌ 데이터 없음: $DATA (git push 했는지, .gitignore 예외가 있는지 확인)"; finish 11; }
echo "데이터: $DATA ($(wc -l < "$DATA")건)"

step "2. 설치 (v4 노트북 설치 셀과 동일한 순서)"
export PIP_DISABLE_PIP_VERSION_CHECK=1 HF_HUB_ENABLE_HF_TRANSFER=1
pip install -q -U pip
pip install -q --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 || finish 20
pip uninstall -q -y torchao || true
pip install -q "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git" || pip install -q unsloth || finish 20
pip install -q --upgrade --force-reinstall --no-cache-dir --no-deps "git+https://github.com/unslothai/unsloth-zoo.git" || finish 20
pip install -q -U datasets accelerate peft trl bitsandbytes hf_transfer huggingface_hub || finish 20
pip install -q -U "transformers>=5.2.0" || pip install -q git+https://github.com/huggingface/transformers.git || finish 20
pip uninstall -q -y torchao || true
python -c "import torch, transformers; print('torch', torch.__version__, '| transformers', transformers.__version__)" || finish 20

step "3. 학습 → 업로드"
python scripts/train_lora.py --version "$VERSION" --hub-repo "${HF_REPO:-}" --out-dir "/workspace/outputs/yunsur_${VERSION}"
RC=$?
[[ $RC -eq 0 ]] && echo "✅ 학습·업로드 완료" || echo "❌ train_lora.py rc=$RC — 어댑터는 /workspace/outputs/yunsur_${VERSION}/adapter 에 남아 있음 (KEEP_POD=1 로 재실행해 회수)"
finish "$RC"
