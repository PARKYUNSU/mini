#!/usr/bin/env python3
"""yunsur LoRA SFT — v4 노트북(finetune_datasets/v4/yunsur_v4_unsloth_finetune.ipynb)을 스크립트로 옮긴 것.

  python scripts/train_lora.py --version v5                                  # 기본: finetune_datasets/v5/train_data_v5.jsonl
  python scripts/train_lora.py --version v5 --hub-repo <user>/yunsur_v5_lora  # 학습 후 HF Hub private 레포 업로드 (HF_TOKEN 환경변수)
  python scripts/train_lora.py --version v5 --max-steps 5 --no-upload         # 스모크

하이퍼파라미터는 HPARAMS 상수로 고정 (v3 = v4 = v5). 바꾸면 "데이터만 바꾼 효과"를 분리할 수 없으므로 CLI 로 열지 않는다.
바꿔야 하면 새 버전 실험 노트에 사유를 적고 이 파일을 수정한다.

예외 하나 — ``LEARNING_RATE`` 환경변수로 lr 만 덮어쓸 수 있다 (기본값은 HPARAMS 그대로 2e-4).
lr 자체가 실험 변수인 라운드를 위한 것이다 (docs/experiments/yunsur_v10/). 소스를 고쳐 박으면
이전 라운드의 재현이 깨지므로 환경변수로 받고, 대신 **조용히 바뀌지 않게** 한다:
기본값과 다르면 배너를 찍고 train_stats.json 의 ``hparam_overrides`` 에 기록한다.
  LEARNING_RATE=5e-5 python scripts/train_lora.py --version v10

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
import shutil
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


def resolve_learning_rate(raw: str | None, default: float) -> tuple[float, dict]:
    """``LEARNING_RATE`` 환경변수를 검증해 (실제 lr, 오버라이드 기록) 을 돌려준다.

    lr 이 실험 변수인 라운드(docs/experiments/yunsur_v10/)를 위한 유일한 예외다.
    소스를 고쳐 박으면 이전 라운드 재현이 깨지므로 환경변수로 받되,
    **조용히 바뀌지 않게** 기본값과 다를 때만 기록을 남긴다 (train_stats.json).
    값이 없거나 기본값과 같으면 기록은 비어 있다.
    """
    if raw is None or not raw.strip():
        return default, {}
    try:
        lr = float(raw.strip())
    except ValueError:
        raise SystemExit(f"LEARNING_RATE 를 float 로 읽을 수 없다: {raw!r}")
    if not 0 < lr < 1:
        raise SystemExit(f"LEARNING_RATE 범위가 이상하다: {lr} (0 < lr < 1)")
    if lr == default:
        return lr, {}
    return lr, {"learning_rate": {"default": default, "used": lr}}


def resolve_max_seq_length(raw: str | None, default: int) -> tuple[int, dict]:
    """``MAX_SEQ_LENGTH`` 환경변수로 최대 길이만 덮어쓴다 (yunsur_v12: 문서 5편이 든 RAG 입력이 2048 을 넘는다).

    더 긴 샘플이 잘리지 않게 할 뿐, 원래 2048 안에 들던 샘플의 학습은 바꾸지 않는다.
    """
    if raw is None or not str(raw).strip():
        return default, {}
    try:
        n = int(str(raw).strip())
    except ValueError:
        raise SystemExit(f"MAX_SEQ_LENGTH 를 정수로 읽을 수 없다: {raw!r}")
    if n < default:
        raise SystemExit(f"MAX_SEQ_LENGTH({n}) 는 기본값({default}) 이상이어야 한다 — 줄이면 기존 샘플이 잘린다")
    return n, ({"max_seq_length": {"default": default, "used": n}} if n != default else {})


# ---------------------------------------------------------------- 0) 환경 검증 (노트북 셀 4)
def resolve_save_steps(raw: str | None, total_hint: int = 138) -> int | None:
    """``SAVE_STEPS`` 환경변수를 검증해 중간 체크포인트 간격을 돌려준다 (없으면 None).

    학습 자체를 바꾸지 않는다 — 어느 시점의 어댑터를 **남기는지**만 정한다. 그래서
    HPARAMS 오버라이드로 기록하지 않고 별도 필드에 적는다.
    """
    if raw is None or not str(raw).strip():
        return None
    try:
        n = int(str(raw).strip())
    except ValueError:
        raise SystemExit(f"SAVE_STEPS 를 정수로 읽을 수 없다: {raw!r}")
    if n < 1:
        raise SystemExit(f"SAVE_STEPS 는 1 이상이어야 한다: {n}")
    if n > total_hint:
        raise SystemExit(f"SAVE_STEPS({n}) 가 전체 스텝({total_hint})보다 크다 — 중간 저장이 하나도 안 생긴다")
    return n


def resolve_save_steps_max(raw: str | None) -> int | None:
    """``SAVE_STEPS_MAX`` — **업로드할** 중간 체크포인트의 스텝 상한 (없으면 전부).

    학습도, 디스크 저장도 바꾸지 않는다. 촘촘한 간격(예 3스텝)으로 저장하면서 관심
    구간만 올릴 때 쓴다 — 46개를 전부 올리면 6GB 이고 파드는 곧 종료된다.
    """
    if raw is None or not str(raw).strip():
        return None
    try:
        n = int(str(raw).strip())
    except ValueError:
        raise SystemExit(f"SAVE_STEPS_MAX 를 정수로 읽을 수 없다: {raw!r}")
    if n < 1:
        raise SystemExit(f"SAVE_STEPS_MAX 는 1 이상이어야 한다: {n}")
    return n


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

    H = dict(HPARAMS)
    lr, hparam_overrides = resolve_learning_rate(os.environ.get("LEARNING_RATE"), HPARAMS["learning_rate"])
    save_steps = resolve_save_steps(os.environ.get("SAVE_STEPS"))
    save_steps_max = resolve_save_steps_max(os.environ.get("SAVE_STEPS_MAX"))
    H["learning_rate"] = lr
    msl, msl_override = resolve_max_seq_length(os.environ.get("MAX_SEQ_LENGTH"), HPARAMS["max_seq_length"])
    H["max_seq_length"] = msl
    hparam_overrides = {**hparam_overrides, **msl_override}
    if hparam_overrides:
        log("=" * 66)
        if "learning_rate" in hparam_overrides:
            log(f"  하이퍼파라미터 오버라이드: learning_rate {HPARAMS['learning_rate']} -> {lr}")
        if msl_override:
            log(f"  하이퍼파라미터 오버라이드: max_seq_length {HPARAMS['max_seq_length']} -> {msl} (잘림 방지)")
        log("  라운드 노트에 사유가 적혀 있어야 한다 (docs/experiments/).")
        log("=" * 66)
    log(f"learning_rate = {lr} ({'LEARNING_RATE 오버라이드' if 'learning_rate' in hparam_overrides else 'HPARAMS 기본값'})")
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

    # 중간 체크포인트 — 기전 라운드에서 "몇 스텝에서 행동이 꺾이나" 를 보려면 필요하다.
    # 끄면(기본) 동작은 v3~v11 과 같다.
    if save_steps:
        sft_kwargs["save_strategy"] = "steps"
        sft_kwargs["save_steps"] = save_steps
        sft_kwargs["save_total_limit"] = None  # 전부 남긴다 — 나중에 고를 수 있게
        log(f"중간 체크포인트: {save_steps} 스텝마다 저장 (save_total_limit 없음)")

    # TRL 0.12+ 는 tokenizer= → processing_class=, TRL 0.20+ 는 dataset_text_field·max_seq_length·
    # packing·dataset_num_proc 를 SFTTrainer 대신 SFTConfig 로 받고 max_seq_length → max_length 로 개명했다.
    # 노트북 시절 인자 이름을 그대로 쓰면 TypeError 로 학습 직전에 죽으므로, 시그니처를 보고 맞춘다.
    import inspect

    cfg_fields = set(inspect.signature(SFTConfig.__init__).parameters)
    trainer_fields = set(inspect.signature(SFTTrainer.__init__).parameters)
    dataset_kwargs = {
        "dataset_text_field": "text",
        "dataset_num_proc": 2,
        "packing": H["packing"],
        ("max_length" if "max_length" in cfg_fields else "max_seq_length"): H["max_seq_length"],
    }
    trainer_kwargs = dict(model=model, train_dataset=dataset)
    trainer_kwargs["processing_class" if "processing_class" in trainer_fields else "tokenizer"] = tokenizer
    for key, value in dataset_kwargs.items():
        if key in cfg_fields:
            sft_kwargs[key] = value
        elif key in trainer_fields:
            trainer_kwargs[key] = value
        else:
            log(f"[경고] SFTConfig/SFTTrainer 둘 다 {key} 를 받지 않음 — 생략")
    log(f"TRL 인자 매핑: config={sorted(k for k in dataset_kwargs if k in sft_kwargs)} "
        f"trainer={sorted(k for k in trainer_kwargs if k != 'model' and k != 'train_dataset')}")
    trainer = SFTTrainer(args=SFTConfig(**sft_kwargs), **trainer_kwargs)
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
        "hparam_overrides": hparam_overrides,
        "save_steps": save_steps,
        "save_steps_max": save_steps_max,
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

    # 8b) 중간 체크포인트 정리 — merge_lora_gguf.sh 가 쓰는 두 파일만 남긴다.
    # 체크포인트 디렉터리에는 옵티마이저·RNG 상태까지 들어 있는데, 우리는 재개가 아니라
    # **머지**만 하므로 필요 없다 (업로드도 그만큼 가벼워진다).
    ckpt_steps: list[int] = []
    if save_steps:
        ckpt_root = out_dir / "checkpoints"
        staged = out_dir / "ckpt_adapters"
        for d in sorted(ckpt_root.glob("checkpoint-*"), key=lambda q: int(q.name.split("-")[-1])):
            step = int(d.name.split("-")[-1])
            if save_steps_max is not None and step > save_steps_max:
                continue  # 저장은 됐지만 올리지 않는다 (SAVE_STEPS_MAX)
            wt = d / "adapter_model.safetensors"
            cfg = d / "adapter_config.json"
            if not wt.is_file() or not cfg.is_file():
                log(f"[경고] checkpoint-{step} 에 어댑터 파일이 없다 — 건너뜀 ({[f.name for f in d.iterdir()][:6]})")
                continue
            dst = staged / f"step-{step:03d}"
            dst.mkdir(parents=True, exist_ok=True)
            shutil.copy2(wt, dst / wt.name)
            shutil.copy2(cfg, dst / cfg.name)
            ckpt_steps.append(step)
        cap = f" (SAVE_STEPS_MAX={save_steps_max} 로 걸러냄)" if save_steps_max else ""
        log(f"중간 체크포인트 정리 완료: {ckpt_steps or '없음'}{cap}")
        summary["ckpt_steps"] = ckpt_steps
        (out_dir / "train_stats.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

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
    for step in ckpt_steps:
        src = out_dir / "ckpt_adapters" / f"step-{step:03d}"
        try:
            api.upload_folder(
                folder_path=str(src), repo_id=args.hub_repo, repo_type="model",
                path_in_repo=f"checkpoints/step-{step:03d}",
                commit_message=f"yunsur_{args.version} checkpoint step {step}",
            )
            log(f"체크포인트 업로드 step {step}")
        except Exception as e:  # 파드가 곧 종료되므로 하나 실패해도 나머지를 계속 올린다
            log(f"[경고] 체크포인트 step {step} 업로드 실패: {type(e).__name__}: {e}")
    log(f"업로드 완료 → https://huggingface.co/{args.hub_repo} (private)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
