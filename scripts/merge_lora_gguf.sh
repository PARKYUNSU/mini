#!/bin/bash
# LoRA 어댑터 → 진짜 베이스(Qwen/Qwen3.5-9B)에 머지 → q4_k_m → Ollama 등록. 맥미니에서 실행.
#   bash "/Volumes/T7 Shield/mini/scripts/merge_lora_gguf.sh" v5          # 어댑터: /Volumes/T7 Shield/yunsur_v5_hub/adapter (HF 다운로드 결과)
#   bash "/Volumes/T7 Shield/mini/scripts/merge_lora_gguf.sh" v4          # 어댑터: mini/yunsur_v4_adapter
#   ADAPTER_DIR=/path/to/adapter bash .../merge_lora_gguf.sh v5           # 경로 직접 지정
#   OLLAMA_TAG=yunsur_v4_merged bash .../merge_lora_gguf.sh v4             # 등록 이름 지정 (운영 중인 yunsur_v4 를 덮어쓰지 않기 위해 v4 는 기본이 _merged)
#
# 왜 머지인가: Ollama 0.34.2 가 `ollama create` 의 `ADAPTER` 를 거부한다 ("LoRA adapters are no longer supported").
# (이전 버전에서 만들어 둔 yunsur_v4 어댑터 모델은 여전히 로드·적용됨 — temperature 0 A/B 로 확인. 그건 운영용으로 유지.)
# 공정 비교를 위해 (1) 베이스는 HF Qwen/Qwen3.5-9B 를 직접 받아 bf16 GGUF 로 만들고 general.name 으로 검증(파일명 신뢰 금지),
# (2) 양자화는 공식 qwen3.5:9b 와 같은 q4_k_m, (3) TEMPLATE·PARAMETER 는 `ollama show qwen3.5:9b --modelfile` 에서 그대로 복사한다.
# 각 단계는 결과 파일이 있으면 건너뛴다 (재실행 안전). 베이스 GGUF 는 한 번 만들면 v4/v5/이후 라운드가 공유.
set -euo pipefail

VERSION="${1:-v5}"
T7="/Volumes/T7 Shield"
MINI="$T7/mini"
case "$VERSION" in
  v4) DEFAULT_ADAPTER="$MINI/yunsur_v4_adapter"; DEFAULT_TAG="yunsur_v4_merged" ;;
  *)  DEFAULT_ADAPTER="$T7/yunsur_${VERSION}_hub/adapter"; DEFAULT_TAG="yunsur_${VERSION}" ;;
esac
ADAPTER="${ADAPTER_DIR:-$DEFAULT_ADAPTER}"
TAG="${OLLAMA_TAG:-$DEFAULT_TAG}"
HF_BASE_ID="Qwen/Qwen3.5-9B"
HF_BASE_DIR="$T7/hf/Qwen3.5-9B"                       # HF 원본 (~18GB, 1회)
BASE_GGUF="$T7/llm/Qwen3.5-9B-base.BF16.gguf"         # 진짜 베이스. (llm/Qwen3.5-9B.BF16.gguf 는 v3 머지본이라 이름을 다르게 둠)
LORA_GGUF="$T7/yunsur_${VERSION}_lora.gguf"
MERGED_GGUF="$T7/yunsur_${VERSION}-bf16.gguf"          # ~18GB, 양자화 후 삭제 가능
Q4_GGUF="$T7/yunsur_${VERSION}-q4_k_m.gguf"           # 최종 (~5.6GB)
MODELFILE="$MINI/Modelfile.${TAG#yunsur_}"
LLAMA_SRC="$HOME/llama.cpp"
VENV="$HOME/llama_venv"
PY="$VENV/bin/python"

step() { echo; echo "===== [$(date '+%H:%M:%S')] $* ====="; }
gguf_name() {  # general.name / architecture 출력
  "$PY" - "$1" <<'PY'
import sys
from gguf import GGUFReader
r = GGUFReader(sys.argv[1])
def s(k):
    f = r.fields.get(k)
    return bytes(f.parts[f.data[0]]).decode("utf-8", "replace") if f else "?"
print(f"general.name={s('general.name')!r} general.architecture={s('general.architecture')!r}")
PY
}

step "0. 사전 확인 — VERSION=$VERSION TAG=$TAG"
if ollama show "$TAG" >/dev/null 2>&1 && [[ "${OVERWRITE:-0}" != "1" ]]; then echo "❌ Ollama 에 $TAG 가 이미 있음 — 덮어쓰려면 OVERWRITE=1"; exit 1; fi
[[ -f "$ADAPTER/adapter_model.safetensors" ]] || { echo "❌ 어댑터 없음: $ADAPTER"; exit 1; }
command -v ollama >/dev/null || { echo "❌ ollama 없음"; exit 1; }
ollama show qwen3.5:9b >/dev/null 2>&1 || { echo "❌ qwen3.5:9b 없음 (템플릿 복사 원본) — ollama pull qwen3.5:9b"; exit 1; }
command -v brew >/dev/null || { echo "❌ Homebrew 없음"; exit 1; }
df -h "$T7" | tail -1

step "1. llama.cpp 소스·빌드 (export-lora, quantize)"
command -v cmake >/dev/null || brew install cmake
if [[ ! -d "$LLAMA_SRC" ]]; then git clone --depth 1 https://github.com/ggml-org/llama.cpp "$LLAMA_SRC"; else (cd "$LLAMA_SRC" && git pull --ff-only || true); fi
BUILD="$LLAMA_SRC/build"; EXPORT_LORA="$BUILD/bin/llama-export-lora"; QUANTIZE="$BUILD/bin/llama-quantize"
if [[ ! -x "$EXPORT_LORA" || ! -x "$QUANTIZE" ]]; then
  cmake -S "$LLAMA_SRC" -B "$BUILD" -DGGML_METAL=ON -DLLAMA_CURL=OFF -DCMAKE_BUILD_TYPE=Release
  cmake --build "$BUILD" --target llama-export-lora llama-quantize -j "$(sysctl -n hw.ncpu)"
fi

step "2. 변환용 venv"
[[ -x "$PY" ]] || python3 -m venv "$VENV"
"$VENV/bin/pip" install -q -U pip
"$VENV/bin/pip" install -q -e "$LLAMA_SRC/gguf-py"
"$VENV/bin/pip" install -q torch numpy safetensors transformers sentencepiece protobuf huggingface_hub hf_transfer

step "3. HF 베이스 원본 다운로드 → $HF_BASE_DIR (1회, ~18GB)"
if [[ ! -f "$HF_BASE_DIR/config.json" ]]; then
  HF_HUB_ENABLE_HF_TRANSFER=1 "$PY" -c "
from huggingface_hub import snapshot_download
snapshot_download('$HF_BASE_ID', local_dir='$HF_BASE_DIR')
print('done')"
fi
ls "$HF_BASE_DIR" | head

step "4. 베이스 bf16 GGUF (1회) + 메타데이터 검증"
if [[ ! -f "$BASE_GGUF" ]]; then
  "$PY" "$LLAMA_SRC/convert_hf_to_gguf.py" "$HF_BASE_DIR" --outtype bf16 --outfile "$BASE_GGUF"
fi
ls -lh "$BASE_GGUF"; META=$(gguf_name "$BASE_GGUF"); echo "$META"
echo "$META" | grep -qi "yunsur" && { echo "❌ 베이스 GGUF 가 yunsur 머지본임 — 중단"; exit 1; }

step "5. 어댑터 → LoRA GGUF"
if [[ ! -f "$LORA_GGUF" ]]; then
  "$PY" "$LLAMA_SRC/convert_lora_to_gguf.py" "$ADAPTER" --base "$HF_BASE_DIR" --outtype f16 --outfile "$LORA_GGUF"
fi
ls -lh "$LORA_GGUF"

step "6. 베이스 + LoRA 머지 (~18GB 쓰기)"
if [[ ! -f "$MERGED_GGUF" ]]; then
  "$EXPORT_LORA" -m "$BASE_GGUF" --lora "$LORA_GGUF" -o "$MERGED_GGUF"
fi
ls -lh "$MERGED_GGUF"

step "7. q4_k_m 양자화 (공식 qwen3.5:9b 와 동일 포맷)"
if [[ ! -f "$Q4_GGUF" ]]; then
  "$QUANTIZE" "$MERGED_GGUF" "$Q4_GGUF" Q4_K_M
fi
ls -lh "$Q4_GGUF"; gguf_name "$Q4_GGUF"

step "8. Modelfile — 공식 qwen3.5:9b 의 TEMPLATE/PARAMETER 복사, FROM 만 교체 → $MODELFILE"
{
  echo "# ${TAG} — Qwen/Qwen3.5-9B 진짜 베이스에 ${VERSION} LoRA 머지 → q4_k_m. TEMPLATE/PARAMETER 는 \`ollama show qwen3.5:9b --modelfile\` 복사 ($(date +%F))."
  echo "# 생성: scripts/merge_lora_gguf.sh ${VERSION}  (Ollama 0.34+ 가 create 의 ADAPTER 를 거부해 머지 방식)"
  echo "FROM \"$Q4_GGUF\""
  ollama show qwen3.5:9b --modelfile | grep -vE '^(FROM|ADAPTER|#) '
} > "$MODELFILE"
head -5 "$MODELFILE"

step "9. Ollama 등록·스모크"
ollama create "$TAG" -f "$MODELFILE"
ollama list | grep -E "yunsur|qwen3.5" || true
ollama run "$TAG" "너 누구야? 한 문장으로." 2>/dev/null | head -5

echo; echo "✅ 완료. 중간 파일 정리(선택): rm \"$MERGED_GGUF\""
