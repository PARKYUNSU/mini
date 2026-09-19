#!/usr/bin/env python3
"""yunsur LoRA SFT — v4 노트북(finetune_datasets/v4/yunsur_v4_unsloth_finetune.ipynb)을 스크립트로 옮긴 것.

  python scripts/train_lora.py --version v5                                  # 기본: finetune_datasets/v5/train_data_v5.jsonl
  python scripts/train_lora.py --version v5 --hub-repo <user>/yunsur_v5_lora  # 학습 후 HF Hub private 레포 업로드 (HF_TOKEN 환경변수)
  python scripts/train_lora.py --version v5 --max-steps 5 --no-upload         # 스모크

하이퍼파라미터는 HPARAMS 상수로 고정 (v3 = v4 = v5). 바꾸면 "데이터만 바꾼 효과"를 분리할 수 없으므로 CLI 로 열지 않는다.
바꿔야 하면 새 버전 실험 노트에 사유를 적고 이 파일을 수정한다.

출력 (--out-dir, 기본 outputs/yunsur_{version})
  adapter/                 — LoRA 어댑터 + 토크나이저 (save_pretrained). 맥미니에서 convert_lora_to_gguf.py 로 변환
  train_log.json           — trainer.state.log_history (loss 추이 → 03_train_config.md)
  train_stats.json         — 데이터 통계(슬롯 분포·system 종류·토큰 길이·잘림) + 하이퍼파라미터 + 학습 시간
GGUF 변환은 Pod 에서 하지 않는다 (v4 때 디스크 부족으로 실패). 맥미니 `ADAPTER` 런타임 적용이 기준.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ── v3 = v4 = v5 고정 (docs/experiments/yunsur_v4/03_train_config.md)
MODEL_NAME = "Qwen/Qwen3.5-9B"  # transformers >= 5.2.0 (qwen3_5)
HPARAMS = {
    "max_seq_length": 2048,
    "load_in_4bit": False,
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0,
    "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    "per_device_train_batch_size": 1,
    "gradient_accumulation_steps": 8,
    "warmup_steps": 10,
    "num_train_epochs": 1,
    "learning_rate": 2e-4,
    "optim": "adamw_8bit",
    "weight_decay": 0.01,
    "lr_scheduler_type": "linear",
    "logging_steps": 10,
    "seed": 3407,
    "packing": False,
    "chat_template": "chatml",
}
INSTRUCTION_MARK = "<|im_start|>user\n"
RESPONSE_MARK = "<|im_start|>assistant\n"
REQUIRED_KEYS = ("slot", "system", "instruction", "output")


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ---------------------------------------------------------------- 0) 환경 검증 (노트북 셀 4)
def check_env() -> None:
    import torch

    _ind = getattr(torch, "_inductor", None)
    if getattr(_ind, "config", None) is None:
        raise RuntimeError(
            "torch._inductor.config 없음 — PyTorch 2.5+ 로 올리고 (cu124 휠) 다시 실행. "
            "unsloth_zoo 가 inspect.getsource(torch._inductor.config) 를 쓴다."
        )
    _pt = getattr(torch.utils, "_pytree", None)
    if _pt is not None and not hasattr(_pt, "register_constant"):
        log("[경고] torch.utils._pytree.register_constant 없음 — torchao 제거(pip uninstall -y torchao) 또는 torch 2.5+")
    import transformers

    major, minor = (int(x) for x in transformers.__version__.split(".")[:2])
    if (major, minor) < (5, 2):
        raise RuntimeError(f"transformers {transformers.__version__} — Qwen3.5(qwen3_5) 는 >= 5.2.0 필요")
    log(f"PyTorch {torch.__version__} | CUDA {torch.version.cuda} | transformers {transformers.__version__} | GPU {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none'}")


# ---------------------------------------------------------------- 1) 데이터 검증 (스크립트 추가: 학습 전에 규약 위반을 잡는다)
def validate_jsonl(path: Path) -> list[dict]:
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        missing = [k for k in REQUIRED_KEYS if not (r.get(k) or "").strip()]
        if missing:
            raise ValueError(f"{path}:{i} 필드 누락/빈 값 {missing} — 데이터 규약 위반")
        rows.append(r)
    if not rows:
        raise ValueError(f"{path}: 레코드 없음")
    return rows


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="v5", help="finetune_datasets/{version}/train_data_{version}.jsonl · outputs/yunsur_{version}")
    ap.add_argument("--data", default="", help="학습 jsonl (기본은 --version 으로 결정)")
    ap.add_argument("--out-dir", default="", help="출력 폴더 (기본 outputs/yunsur_{version})")
    ap.add_argument("--model-name", default=MODEL_NAME)
    ap.add_argument("--hub-repo", default=os.environ.get("HF_REPO", ""), help="HF Hub 업로드 대상 (예: user/yunsur_v5_lora). 없으면 업로드 생략")
    ap.add_argument("--no-upload", action="store_true")
    ap.add_argument("--max-steps", type=int, default=0, help="스모크용. 0 이면 1 epoch 전체")
    args = ap.parse_args()

    data_path = Path(args.data) if args.data else ROOT / "finetune_datasets" / args.version / f"train_data_{args.version}.jsonl"
    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "outputs" / f"yunsur_{args.version}"
    adapter_dir = out_dir / "adapter"
    out_dir.mkdir(parents=True, exist_ok=True)
    if not data_path.is_file():
        raise FileNotFoundError(f"데이터 없음: {data_path}")

    os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")
    check_env()
    raw_rows = validate_jsonl(data_path)
    log(f"데이터 {data_path} — {len(raw_rows)}건, 슬롯 {dict(Counter(r['slot'] for r in raw_rows))}, system {len(set(r['system'] for r in raw_rows))}종")

    import torch
    from datasets import load_dataset
    from trl import SFTConfig, SFTTrainer
    from unsloth import FastLanguageModel
    from unsloth.chat_templates import get_chat_template, standardize_sharegpt, train_on_responses_only

    H = HPARAMS
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16

    # 2) 모델 로드 (셀 9)
    log(f"베이스 모델 로드 {args.model_name} ({dtype})")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model_name,
        max_seq_length=H["max_seq_length"],
        dtype=dtype,
        load_in_4bit=H["load_in_4bit"],
    )

    # 3) LoRA (셀 11)
    model = FastLanguageModel.get_peft_model(
        model,
        r=H["lora_r"],
        target_modules=H["target_modules"],
        lora_alpha=H["lora_alpha"],
        lora_dropout=H["lora_dropout"],
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=H["seed"],
    )

    # 4) ChatML + ShareGPT (셀 13~14). system 은 레코드 필드 그대로 — 단일 페르소나 덮어쓰기 금지
    tokenizer = get_chat_template(
        tokenizer,
        chat_template=H["chat_template"],
        mapping={"role": "from", "content": "value", "user": "human", "assistant": "gpt"},
    )

    def convert_to_sharegpt(examples):
        convos = []
        for system, instruction, output in zip(examples["system"], examples["instruction"], examples["output"]):
            assert system and system.strip(), "system 이 비어 있는 레코드"
            convos.append(
                [
                    {"from": "system", "value": system},
                    {"from": "human", "value": instruction},
                    {"from": "gpt", "value": output},
                ]
            )
        return {"conversations": convos}

    def formatting_prompts_func(examples):
        return {"text": [tokenizer.apply_chat_template(c, tokenize=False, add_generation_prompt=False) for c in examples["conversations"]]}

    dataset = load_dataset("json", data_files=str(data_path.resolve()), split="train")
    dataset = dataset.map(convert_to_sharegpt, batched=True)
    dataset = standardize_sharegpt(dataset)
    dataset = dataset.map(formatting_prompts_func, batched=True)

    _tok = getattr(tokenizer, "tokenizer", tokenizer)  # Qwen3.5 는 Processor — text= 키워드로
    lens = sorted(len(_tok(text=t)["input_ids"]) for t in dataset["text"])
    data_stats = {
        "samples": len(dataset),
        "slot_dist": dict(Counter(r["slot"] for r in raw_rows)),
        "system_kinds": len(set(r["system"] for r in raw_rows)),
        "token_len_median": lens[len(lens) // 2],
        "token_len_p95": lens[int(len(lens) * 0.95)],
        "token_len_max": lens[-1],
        "truncated": sum(1 for l in lens if l > H["max_seq_length"]),
    }
    log(f"토큰 길이 중앙값 {data_stats['token_len_median']} / p95 {data_stats['token_len_p95']} / max {data_stats['token_len_max']} / 잘림 {data_stats['truncated']}")

    # 5) 마스킹 delimiter 검증 (셀 16~17)
    sample = dataset[0]["text"]
    if RESPONSE_MARK not in sample or INSTRUCTION_MARK not in sample:
        print(repr(sample[:1200]))
        raise RuntimeError(f"템플릿에 {INSTRUCTION_MARK!r}/{RESPONSE_MARK!r} 없음 — chat_template 확인")
    log("마스킹 delimiter 검증 OK")

    # 6) Trainer (셀 19)
    sft_kwargs = dict(
        per_device_train_batch_size=H["per_device_train_batch_size"],
        gradient_accumulation_steps=H["gradient_accumulation_steps"],
        warmup_steps=H["warmup_steps"],
        num_train_epochs=H["num_train_epochs"],
        learning_rate=H["learning_rate"],
        fp16=dtype is torch.float16,
        bf16=dtype is torch.bfloat16,
        logging_steps=H["logging_steps"],
        optim=H["optim"],
        weight_decay=H["weight_decay"],
        lr_scheduler_type=H["lr_scheduler_type"],
        seed=H["seed"],
        output_dir=str(out_dir / "checkpoints"),
        report_to="none",
    )
    if args.max_steps:
        sft_kwargs["max_steps"] = args.max_steps
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=H["max_seq_length"],
        dataset_num_proc=2,
        packing=H["packing"],
        args=SFTConfig(**sft_kwargs),
    )
    trainer = train_on_responses_only(trainer, instruction_part=INSTRUCTION_MARK, response_part=RESPONSE_MARK)

    # 7) 학습 (셀 20)
    log("학습 시작")
    t0 = time.time()
    trainer_stats = trainer.train()
    elapsed = time.time() - t0
    hist = [h for h in trainer.state.log_history if "loss" in h]
    (out_dir / "train_log.json").write_text(json.dumps(trainer.state.log_history, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {
        "version": args.version,
        "model_name": args.model_name,
        "data_file": str(data_path.relative_to(ROOT)) if data_path.is_relative_to(ROOT) else str(data_path),
        "data": data_stats,
        "hparams": H,
        "dtype": str(dtype),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "global_step": trainer.state.global_step,
        "loss_first": hist[0]["loss"] if hist else None,
        "loss_last": hist[-1]["loss"] if hist else None,
        "loss_mean": round(sum(h["loss"] for h in hist) / len(hist), 4) if hist else None,
        "train_runtime_sec": round(elapsed, 1),
        "train_samples_per_second": getattr(trainer_stats, "metrics", {}).get("train_samples_per_second"),
    }
    (out_dir / "train_stats.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"학습 완료 step {summary['global_step']} / loss {summary['loss_first']} → {summary['loss_last']} / {elapsed / 60:.1f}분")

    # 8) 저장 (셀 22) — 어댑터만. GGUF 는 맥미니에서
    adapter_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(adapter_dir))
    tokenizer.save_pretrained(str(adapter_dir))
    log(f"어댑터 저장 {adapter_dir}")

    # 9) HF Hub private 업로드 — 토큰은 HF_TOKEN 환경변수(RunPod Secret)만. 출력에 절대 찍지 않는다.
    if args.no_upload or not args.hub_repo:
        log("업로드 생략" + ("" if args.hub_repo else " (--hub-repo / HF_REPO 없음)"))
        return 0
    if not os.environ.get("HF_TOKEN"):
        log("❌ HF_TOKEN 없음 — 업로드 불가. 어댑터는 로컬에 남아 있음")
        return 2
    from huggingface_hub import HfApi

    api = HfApi()
    api.create_repo(args.hub_repo, repo_type="model", private=True, exist_ok=True)
    api.upload_folder(folder_path=str(adapter_dir), repo_id=args.hub_repo, repo_type="model", path_in_repo="adapter", commit_message=f"yunsur_{args.version} LoRA adapter")
    for f in ("train_log.json", "train_stats.json"):
        api.upload_file(path_or_fileobj=str(out_dir / f), path_in_repo=f, repo_id=args.hub_repo, repo_type="model")
    log(f"업로드 완료 → https://huggingface.co/{args.hub_repo} (private)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
