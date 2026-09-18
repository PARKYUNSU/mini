#!/bin/bash
# yunsur_v4: LoRA 어댑터 → 베이스 BF16 GGUF 에 머지 → q4_k_m 양자화 → Ollama 등록
# 맥미니에서 실행:  bash "/Volumes/T7 Shield/mini/scripts/convert_v4_gguf.sh"
# 각 단계는 결과 파일이 있으면 건너뛰므로 중간에 끊겨도 다시 실행하면 이어짐.
set -euo pipefail

T7="/Volumes/T7 Shield"
MINI="$T7/mini"
ADAPTER="$MINI/yunsur_v4_adapter"
BASE_GGUF="$T7/llm/Qwen3.5-9B.BF16.gguf"
LORA_GGUF="$T7/yunsur_v4_lora.gguf"          # 어댑터만 GGUF 로 (~230MB)
MERGED_GGUF="$T7/yunsur_v4-bf16.gguf"        # 베이스+어댑터 머지 (~18GB, 양자화 후 삭제 가능)
Q4_GGUF="$T7/yunsur_v4-q4_k_m.gguf"          # 최종 (~5.6GB) — Modelfile.v4 의 FROM 과 일치
LLAMA_SRC="$HOME/llama.cpp"                  # convert 스크립트용 소스 (내장 디스크)
VENV="$HOME/llama_venv"                      # 변환 전용 venv (봇 venv 와 분리)

step() { echo; echo "===== $* ====="; }

step "0. 사전 확인"
[[ -f "$ADAPTER/adapter_model.safetensors" ]] || { echo "❌ 어댑터 없음: $ADAPTER"; exit 1; }
[[ -f "$BASE_GGUF" ]] || { echo "❌ 베이스 GGUF 없음: $BASE_GGUF"; exit 1; }
command -v brew >/dev/null || { echo "❌ Homebrew 없음"; exit 1; }

step "1. 빌드 도구 (cmake)"
command -v cmake >/dev/null || brew install cmake

step "2. llama.cpp 소스 (convert_lora_to_gguf.py 용)"
if [[ ! -d "$LLAMA_SRC" ]]; then
  git clone --depth 1 https://github.com/ggml-org/llama.cpp "$LLAMA_SRC"
else
  (cd "$LLAMA_SRC" && git pull --ff-only || true)
fi

step "2b. llama-export-lora / llama-quantize 소스 빌드 (brew 패키지엔 export-lora 가 없음)"
BUILD="$LLAMA_SRC/build"
EXPORT_LORA="$BUILD/bin/llama-export-lora"
QUANTIZE="$BUILD/bin/llama-quantize"
if [[ ! -x "$EXPORT_LORA" || ! -x "$QUANTIZE" ]]; then
  cmake -S "$LLAMA_SRC" -B "$BUILD" -DGGML_METAL=ON -DLLAMA_CURL=OFF -DCMAKE_BUILD_TYPE=Release
  cmake --build "$BUILD" --target llama-export-lora llama-quantize -j "$(sysctl -n hw.ncpu)"
fi
ls -lh "$EXPORT_LORA" "$QUANTIZE"

step "3. 변환용 venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install -q -U pip
"$VENV/bin/pip" install -q -e "$LLAMA_SRC/gguf-py"
"$VENV/bin/pip" install -q torch numpy safetensors transformers sentencepiece protobuf huggingface_hub

step "4. 어댑터 → LoRA GGUF"
if [[ ! -f "$LORA_GGUF" ]]; then
  # --base-model-id: 베이스 config.json 만 HF 에서 받아 텐서 이름/모양을 맞춤 (가중치 다운로드 아님)
  "$VENV/bin/python" "$LLAMA_SRC/convert_lora_to_gguf.py" "$ADAPTER" \
    --base-model-id Qwen/Qwen3.5-9B --outtype f16 --outfile "$LORA_GGUF"
fi
ls -lh "$LORA_GGUF"

step "5. 베이스 BF16 + LoRA 머지 (~18GB 쓰기, 몇 분)"
if [[ ! -f "$MERGED_GGUF" ]]; then
  "$EXPORT_LORA" -m "$BASE_GGUF" --lora "$LORA_GGUF" -o "$MERGED_GGUF"
fi
ls -lh "$MERGED_GGUF"

step "6. q4_k_m 양자화 (v3 배포와 동일 포맷)"
if [[ ! -f "$Q4_GGUF" ]]; then
  "$QUANTIZE" "$MERGED_GGUF" "$Q4_GGUF" Q4_K_M
fi
ls -lh "$Q4_GGUF"

step "7. Ollama 등록"
cd "$MINI"
ollama create yunsur_v4 -f Modelfile.v4
ollama list | grep -E "yunsur|qwen3.5" || true

step "8. 스모크"
ollama run yunsur_v4 "너 누구야? 한 문장으로." 2>/dev/null | head -5

echo
echo "✅ 완료. 머지 중간 파일(18GB)은 필요 없으면 삭제: rm \"$MERGED_GGUF\""
