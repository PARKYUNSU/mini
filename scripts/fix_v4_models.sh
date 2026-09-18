#!/bin/bash
# 잘못 머지된 yunsur_v4 / v2 를 v3 로 오인한 yunsur_v3_q4 를 정리하고 올바르게 재생성
set -euo pipefail
T7="/Volumes/T7 Shield"; MINI="$T7/mini"; cd "$MINI"
QUANTIZE="$HOME/llama.cpp/build/bin/llama-quantize"
V3_BF16="$T7/llm/Qwen3.5-9B.BF16.gguf"      # 실제로는 Yunsur_V3_Model (v3 머지 bf16)
V3_Q4="$T7/yunsur_v3-q4_k_m.gguf"

echo "== 1. 잘못된 모델·파일 제거 =="
ollama rm yunsur_v4 2>/dev/null || true
ollama rm yunsur_v3_q4 2>/dev/null || true
rm -f "$T7/yunsur_v4-bf16.gguf" "$T7/yunsur_v4-q4_k_m.gguf"   # v3 위에 잘못 머지된 것
rm -f "$V3_Q4"                                                 # 실제로는 v2(qwen35-merged-f16) 양자화본

echo "== 2. yunsur_v4 = qwen3.5:9b + v4 어댑터 =="
ollama create yunsur_v4 -f Modelfile.v4

echo "== 3. yunsur_v3_q4 = 진짜 v3 bf16 → q4_k_m (v4 와 동일 양자화) =="
"$QUANTIZE" "$V3_BF16" "$V3_Q4" Q4_K_M
sed "s|^FROM .*|FROM \"$V3_Q4\"|" Modelfile > /tmp/Modelfile.v3q4
ollama create yunsur_v3_q4 -f /tmp/Modelfile.v3q4

echo "== 4. 확인 =="
ollama list | grep -E "yunsur|qwen3.5"
for m in yunsur_v4 yunsur_v3_q4; do
  echo "--- $m ---"; ollama run "$m" "너 누구야? 한 문장으로." 2>/dev/null | head -3
done
