# 새 맥미니(M5 Pro · 64GB) 옮기기와 모델 비교 계획 (2026-11-05)

> 계획 문서다. 아직 바꾼 것도 잰 것도 없다. 배송 예정은 11-11~18 이다. 현재 구성은 11-05 에 16GB 맥미니에서 읽기 전용으로 확인했고, 모델 크기는 같은 날 Ollama 라이브러리 페이지에서 봤다. 새 기기의 속도와 메모리는 미측정이다.

## 0. 한눈에

| 단계 | 내용 | 사람 손 | 맥미니 시간(추정) | Claude 사용량(추정) |
|---|---|---|---|---|
| 1 | 도착 전 준비 (§2) | 결정 3개 남음 (§8) | — | 작음 |
| 2 | 옮기기 (§3) | 초기 설정 · 권한 · T7 옮겨 꽂기 | 반나절, 봇 멈춤 1시간 안팎 | 작음 |
| 3 | 같은 설정 기준선 (§4) | 없음 | 1시간 | 작음 |
| 4 | 후보 속도 (§6.1) | 내려받기 승인 | 후보당 10분 | 작음 |
| 5 | 판단 재생 (§6.2) | 없음 | 후보당 1~2시간 | 라벨 재사용이라 작음 |
| 6 | 큰 모델 dev (§6.3) | 없음 | 후보당 1시간 | 주간 10~15% |
| 7 | held-out 판정 (§6.4) | 운영 반영 승인 | 약 5시간 | 주간 30% 안팎 |
| 8 | 접어 둔 라운드 (§7) | 라운드마다 결정 | 라운드마다 | 라운드마다 |
| 9 | 옛 맥미니 정리 (§9) | 사용자 결정 | — | — |

판단 재생을 답 비교보다 앞에 둔다. 라벨이 이미 있어 가장 싸고, 큰 모델이 9B 의 판단 손실을 줄이는지에 바로 답하기 때문이다. 사용량 추정은 이번 주 라벨 묶음 두 개(합 0.67MB)와 주간 사용량 변화(51 → 60%, 다른 작업 포함)로 어림했다. 7 · 8 은 주간 한도 리셋(11-10 02:00) 뒤에 한다.

## 1. 지금 구성 (11-05 확인)

계정 이름 `yunsupark` 와 볼륨 이름 `T7 Shield` 를 유지하면 경로를 고치지 않아도 된다. docs 밖 41개 파일에 `/Volumes/T7 Shield` 또는 `/Users/...` 가 박혀 있다.

| 무엇 | 지금 위치 | 새 기기에서 |
|---|---|---|
| 코드 · `.env` · `.bridge` · `.venv` · Chroma(`mini-chroma-rebuild2`) · 임베딩 캐시 · GGUF | T7 | 디스크를 옮기면 같이 간다 |
| Ollama 모델 12GB (`yunsur_v13` · `qwen3.5:9b` · `yunsur_v4`) | `~/.ollama/models` | 통째로 복사한다. `yunsur_v4` 는 ADAPTER 방식이라 다시 못 만든다 |
| Ollama 서버 0.40.9 | `/Applications/Ollama.app` | 같은 버전 앱만 설치한다 |
| brew `ollama` (CLI 0.34.2, `sh.brew.ollama` 는 exit 1) | `/opt/homebrew` | 옮기지 않는다. 그 plist 의 `OLLAMA_FLASH_ATTENTION` · `OLLAMA_KV_CACHE_TYPE` 는 지금 서버에 적용되지 않는다 |
| Python 3.12.13 | brew `python@3.12`, `.venv` 가 `/opt/homebrew/opt/python@3.12` 를 가리킴 | 같은 경로로 brew 설치한다 |
| 대화 기록 DB 62MB | `~/Library/Application Support/mini-agent/agent_checkpoints.db*` | 봇을 멈춘 뒤 세 파일을 복사한다 |
| launchd | `com.mini.chroma` · `com.mini.runscheduler` · `com.mini.telegrambot`, 기동기 `~/Library/Application Support/mini/` | 복사한다. 사본은 `ops/launchd/` |
| 별도 서비스 | `com.yunsupark.chatbot` → `~/bin/chatbot_service.sh` → T7 `chatbot_dev`, 포트 8081 | 결정 3 |
| 임베딩 · 재순위 모델 3.3GB | `~/.cache/huggingface` | 복사한다 |
| 기타 | `~/.config/gh` · `~/.config/openresearch*` · `~/orx` · `~/backups`. LoRA 머지 때만 `~/llama.cpp` · `~/llama_venv` | 복사한다 |
| 접속 | 맥북 `~/.ssh/config` `Host mini` = Tailscale `100.101.238.38`, 맥북 `/Volumes/T7 Shield` = `//YUNSU의 Mac mini._smb._tcp.local/T7 Shield` | IP 를 고친다. 컴퓨터 이름 · 공유 이름이 같으면 마운트 주소는 그대로다 |
| 전원 · 로그인 | `sleep 0` · `autorestart 1`, FileVault 켜짐, 자동 로그인 없음 | `pmset` 를 같게 둔다. 결정 2 |

**옮기지 않는 것:** `com.mini.run-scheduler`(옛 파일, 안 올라가 있음), crontab 4줄(T7 권한 문제로 매일 실패, 같은 작업은 스케줄러 쪽), 게임 · 기타 앱(필요할 때 사용자가 설치).

**옮기기 전 값:** Chroma `arxiv_papers` 1,427,191 · `paper_questions` 56,032(컷오버 직전에 다시 읽는다), chromadb 1.5.5 · torch 2.11.0, 패키지 177개([`pip_freeze_m2.txt`](pip_freeze_m2.txt)), T7 은 APFS · 소유권 무시 · USB.

## 2. 도착 전 할 일

- **커밋 백업:** `~/backups/mini/mini-2026-11-05.bundle`(96bafaa, 복원 대조 통과)이 있다. 컷오버 직전에 다시 만든다. 커밋 안 된 파일 613개(77MB)는 T7 에만 있다.
- **옛 기기 기준선:** 일요일 04:00 주간 점검이 [`foundation_1031/weekly.md`](../foundation_1031/weekly.md) 에 쌓는다. 옮기기 전 마지막 행을 기준으로 쓴다(11-08 또는 11-15). 지금까지 응답 중앙 80.3s · 77.8s, 검색 · 답 정답 31/34 다.
- **새 질문:** 사용자가 봇에 실제로 묻는 질문을 모은다. held-out 을 다시 채울 재료이고, 빈 줄 수정과 `RAG_NAME_LOOKUP` 을 실제 답에서 확인하는 일도 겸한다.
- **사용자 결정:** §8.

## 3. 옮기는 순서

**규칙.** 봇은 한 기기에서만 돈다(같은 토큰을 두 곳에서 폴링하면 409). T7 은 Chroma 와 봇을 멈춘 뒤에만 뺀다. 01:00 수집과 측정 중에는 시작하지 않는다. Migration Assistant 는 쓰지 않는다. 실패 중인 crontab · plist 까지 따라온다.

### A. 옛 기기를 돌린 채 준비 (T7 은 옛 기기에)

1. [사용자] 초기 설정. 계정 짧은 이름 `yunsupark`, 컴퓨터 이름은 임시로 `mini-new`.
2. [사용자] 원격 로그인 켜기 + 원격 사용자 전체 디스크 접근 허용, 파일 공유 켜기, Tailscale 로그인, `sudo pmset -a sleep 0 autorestart 1`, Homebrew 설치, 맥북에서 `ssh-copy-id -i ~/.ssh/id_ed25519_macmini.pub yunsupark@<새 IP>`.
3. [Claude] `brew install python@3.12 gh tesseract node cmake`. `python3.12 -V` 가 3.12.13 과 다르면 기록한다.
4. [사용자 승인 후 Claude] Ollama 앱 0.40.9 설치. 내려받기는 파일 · 출처 · 크기를 밝혀 승인받는다.
5. [Claude] 옛 기기에서 §1 의 복사 항목을 `rsync -a` 로 민다. `ollama list` 의 ID 가 옛 기기와 같은지 본다(`a3f87df755a9` · `6488c96fa5fa` · `49be6319a1f5`).

### B. 컷오버 (봇 멈춤)

6. [Claude] 측정 · 수집이 없는지 확인하고, Chroma 수를 읽고, 번들을 다시 만든다.
7. [Claude] 옛 기기에서 멈춘다. 순서를 지킨다.
   ```bash
   launchctl bootout gui/$(id -u)/com.mini.telegrambot
   launchctl bootout gui/$(id -u)/com.mini.runscheduler
   pkill -f apps.telegram_bot.telegram_receiver; pkill -f apps.telegram_bot.ai_worker
   launchctl bootout gui/$(id -u)/com.yunsupark.chatbot
   launchctl bootout gui/$(id -u)/com.mini.chroma
   ```
8. [Claude] 대화 기록 DB 세 파일을 복사하고 `diskutil eject "/Volumes/T7 Shield"`. 이때 맥북의 공유 마운트가 끊기고, 그 경로에서 도는 세션도 멈춘다.
9. [사용자] T7 을 새 기기에 꽂는다. 옛 기기 이름을 `mini-old`, 새 기기 이름을 `YUNSU의 Mac mini` 로 바꾼다. T7 을 공유 이름 `T7 Shield` 로 공유한다. 맥북 `Host mini` 의 `HostName` 을 새 Tailscale IP 로 고치고 다시 마운트한다.
10. [Claude] `.venv` 를 확인한다. 실패하면 [`pip_freeze_m2.txt`](pip_freeze_m2.txt) 로 다시 만든다(chromadb 는 같은 버전으로).
    ```bash
    .venv/bin/python -c "import torch, chromadb, pymupdf4llm, sentence_transformers; print(chromadb.__version__, torch.__version__, torch.backends.mps.is_available())"
    ```
11. [Claude] Chroma 를 올리고 수를 대조한다.
    ```bash
    launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.mini.chroma.plist
    curl -s http://127.0.0.1:8001/api/v2/heartbeat
    .venv/bin/python -c "import chromadb; c=chromadb.HttpClient(host='127.0.0.1',port=8001); print([(x.name,x.count()) for x in c.list_collections()])"
    ```
12. [사용자, 화면 필요] launchd 의 Python 이 T7 을 처음 읽을 때 뜨는 권한 창을 허용한다. launchd 의 bash 는 T7 을 못 읽어 기동기가 venv Python 을 쓴다(`ops/launchd/README.md`).
13. [Claude] 컨텍스트를 4096 으로 고정한다. Ollama 기본값은 VRAM 24GiB 미만 4k · 24~48GiB 32k · 48GiB 이상 256k 다. 새 기기는 어느 칸인지 미확인이고, 그대로 두면 큰 KV 캐시로 시간과 메모리가 달라진다. 앱 설정 슬라이더나 `OLLAMA_CONTEXT_LENGTH` 로 맞추고, `ollama ps` 의 CONTEXT 와 PROCESSOR(100% GPU)로 확인한다.
14. [Claude] 3문항으로 답까지 돌려 오류가 없는지 본다(`eval_e2e_ko.py --answer --ids ...`).
15. [Claude] 스케줄러와 봇을 올린다. [사용자] 텔레그램으로 질문 하나를 보낸다. `bot_receiver.log` 에 409 가 없는지 본다.

### C. 되돌리기

새 기기 launchd 를 `bootout` 한다 → T7 을 옛 기기로 옮긴다 → 옛 기기에서 `bootstrap` 세 개와 `bash restart.sh` → 맥북 `HostName` 을 되돌린다. 대화 기록 DB 는 새 기기에서 다시 복사한다. 옛 기기는 §9 까지 지우지 않는다.

## 4. 같은 설정 기준선

바꾸는 것은 기기뿐이다. 모델 · `.env` · 컨텍스트 4096 · Ollama 0.40.9 를 그대로 둔다. 스케줄러가 켜지면 당일 놓친 작업을 보충 실행하므로 수집이 끝난 뒤에 잰다.

```bash
sh scripts/weekly_check.sh
```

- 검색 정답 · 답 정답 인용 · 오류 · 컨텍스트 밖 인용이 옮기기 전 마지막 행에서 ±1 넘게 벗어나면 멈추고 원인부터 찾는다. 옮기기 문제일 수 있다.
- 시간은 새 기준선이다. 옛 수치와 섞지 않고, 이후 시간 관문은 모두 이 값을 쓴다. 단계별 시간과 `ollama ps` 로 base · v13 이 같이 상주하는지 함께 적는다.

## 5. 후보 모델 (11-05 Ollama 라이브러리)

| 후보 | 태그 | 크기 | 입력 | 까닭 |
|---|---|---|---|---|
| 기준 | `yunsur_v13` | 5.8GB | — | 지금 운영 |
| A | `qwen3.6:27b-q4_K_M` | 17GB | 글 · 이미지 | 같은 계열 dense 큰 모델 |
| B | `qwen3.6:35b-a3b-q4_K_M` | 24GB | 글 · 이미지 | MoE. 활성 파라미터가 적어 A 보다 빠를 수 있다(미측정) |
| C | `llama3.3:70b-instruct-q4_K_M` | 43GB | 글만 | 사용자 요청 70B Q4. Ollama 에서 확인한 70B 급은 이것이다 |

- 내려받기는 합 84GB 이고 내장 512GB 에 들어간다. 파일 · 출처 · 크기를 밝혀 그때 승인받는다.
- C 와 v13 을 같이 올리면 약 49GB 로 기본 GPU 한도(약 48GB) 근처다. 한도를 올리는 `iogpu.wired_limit_mb` 는 시스템 설정이라 사용자가 하고, 재부팅하면 풀린다.
- 빼는 것: `qwen3.5:27b` · `35b`(같은 크기의 이전 판), `qwen3.5:122b-a10b`(81GB, 메모리 초과). MLX 태그는 양자화가 달라 속도 확인 뒤 따로 본다.
- 미확인: 0.40.9 에서 `qwen3.6` 이 도는지(안 되면 Ollama 버전을 올리고 §4 를 다시 잰다), 라이선스, 한국어 성능.

## 6. 모델 비교 (사전 등록 초안)

단계마다 측정 전에 자기 README 로 고정한다. 모델 변수가 가르는 호출은 다음과 같다(코드 확인).

| 변수 | 쓰는 호출 | 비교에서 |
|---|---|---|
| `RAG_ANSWER_MODEL` | 답 · 거르기 · 판정 · 결론 다시 쓰기 | **이것을 후보로 바꾼다** |
| `RAG_HELPER_MODEL` | 라우터 분류 · 검색어 | `yunsur_v13` 유지. 검색어가 바뀌면 검색까지 달라진다 |
| `LOCAL_LLM_MODEL` | 잡담 · 계획 · 코딩 폴백 | 바꾸지 않는다 |

**답만 큰 모델로 바꾸는 것은 환경변수로 안 된다.** `RAG_ANSWER_MODEL` 하나가 거르기 · 판정 · 결론까지 정한다. 평가에는 `EVAL_ANSWER_OPENAI_URL` 경로가 있지만 상한선 비교용 매개변수(`reasoning_effort` medium · `max_tokens` 6000 · temperature 0.2)라 운영과 다르고, 운영에 쓰려면 슬롯을 나누는 코드가 필요하다. 그래서 기본 비교는 코드 변경이 없는 `RAG_ANSWER_MODEL` 교체다.

`.env` 는 건드리지 않고 셸 환경변수로 덮는다. 11-05 에 `RAG_ANSWER_MODEL` · `RAG_HELPER_MODEL` 을 가짜 값으로 덮어 평가 스크립트 경로의 설정값 · 답 LLM · 라우터 LLM 에 반영되는 것을 확인했다. 스케줄러 경로는 `.env` 가 이기므로(`override=True`) 주간 점검에는 통하지 않는다.

```bash
RAG_ANSWER_MODEL=qwen3.6:27b-q4_K_M .venv/bin/python scripts/eval_e2e_ko.py --answer --save-context \
  --questions docs/experiments/real_eval_1013/questions.tsv --gold docs/experiments/real_eval_1013/gold.jsonl --label nm_a_real40
```

### 6.1 속도 — 라벨 없음

real40 앞 5문항(`--ids N01,N02,N03,N04,N05`)을 답까지 돌린다. `ollama ps` 가 100% GPU 이고 스왑이 늘지 않아야 한다. **응답 중앙이 120s 를 넘으면 후보에서 뺀다(사용자 결정 11-05).** 70B 는 여기서 갈린다.

### 6.2 판단 재생 — 라벨 재사용

라벨이 있는 입력에 거르기 · 판정 호출만 다시 돌린다. 두 도구 모두 `RAG_ANSWER_MODEL` 을 읽는다.

| 도구 | 9B 값 | 나아졌다고 볼 기준 |
|---|---|---|
| 거르기 [`topic_filter_1104/pool.py`](../topic_filter_1104/pool.py) `filter` · `score` | 상위 5편 정밀도 49.3% · 재현율 82.6% | 정밀도 ≥ 60% · 재현율 ≥ 78% |
| 판정 [`open_judge_1103/oj.py`](../open_judge_1103/oj.py) `run` · `score` | G1 · G3 통과, G2 미달(4/7, 5/10) | G1 ≥ 70% · G2 ≤ 20% · G3 ≤ 3 (같은 기준) |

- **함정:** 두 도구의 출력 파일 이름이 고정이고 `filter` 는 이어 하기다. 그대로 돌리면 저장된 9B 결과를 건너뛰거나 덮는다. 먼저 출력 이름에 모델 접미사를 붙인다.
- 판정에서 새로 '없음' 이 나온 문항만 `oj.py extra` 로 라벨을 더 단다.
- 이 단계는 진단이고 탈락 기준이 아니다. 둘 다 기준을 넘으면 §6.3 은 `RAG_ANSWER_MODEL` 교체만 잰다. 미달이면 큰 모델이 판단을 고치지 못한다는 뜻이므로, §6.3 에 '답만 큰 모델' 조건을 더한다(먼저 `_openai_answer` 매개변수를 운영과 맞춘다. 결론 다시 쓰기는 v13 으로 남는다).

### 6.3 큰 모델 dev

- **조건:** `RAG_ANSWER_MODEL` 을 후보로 바꾼다. real40 40문항. 거르기가 달라져 문서도 달라질 수 있다. 입력이 같은 문항 수는 `answer_input` 으로 적되, 모델이 다르므로 빼지 않는다.
- **라벨:** 문항마다 두 조건의 문서(겹치면 한 번)와 답을 무작위 순서로 한 묶음에 넣고 모델을 가린다. 답마다 E+X(과장 + 사실 오류) 수를 센다.
- **자동 지표:** 답 본문 정답 인용, '없음' 답, 컨텍스트 밖 인용, 한자 · 영어 섞임, 줄바꿈 깨짐, 잘림, 단계별 시간. v13 은 형식을 학습한 모델이라 큰 모델의 형식 실패가 첫 위험이다.
- **기준:** E+X 가 적은 문항 : 많은 문항 ≥ 2:1, 답 정답 인용 −2 이내, 컨텍스트 밖 인용 +1 이내. 통과한 후보 중 우위가 큰 쪽 하나만 올린다(같으면 빠른 쪽).
- dev 통과는 채택 근거가 아니다. 아무도 못 넘으면 운영은 v13 그대로이고 빨라진 시간만 얻는다.

### 6.4 held-out 판정

- **조건:** 지금 설정 대 §6.3 승자 설정. 측정 전에 하나로 고정한다.
- **문항:** [`foundation_1031/heldout.tsv`](../foundation_1031/heldout.tsv) 90문항. 대조 재실행 15문항을 눈가림으로 섞어 같은 모델끼리의 흔들림도 잰다.
- **주 지표:** 문항별 E+X 수, 적으면 승. 양측 부호 검정 p < 0.05.
- **문항 수(§2.5):** 예상 효과 3:1, 동점 30% 면 동점 뺀 문항이 약 63 이다. 2:1(37 필요)까지 잡는다.

| 보호 지표 | 기준 |
|---|---|
| 본문 인용 중 '2' 비율 | 처리 ≥ 대조 − 5%p |
| 컨텍스트 밖 인용 | 처리 ≤ 대조 + 1 |
| 거짓 '없음' · 거짓 '있음' | 각각 처리 ≤ 대조 + 2 |
| 한자 · 영어 섞임 · 줄바꿈 깨짐 · 잘림 | 합 처리 ≤ 대조 + 2 |
| 응답 시간 중앙 | ≤ 120s |
| 오류 · 스왑 | 오류 0, 측정 중 스왑 증가 없음 |

- **채택:** 모두 통과하면 사용자 승인을 받아 `.env` 를 바꾸고 봇을 재시작한다. 미달이면 운영은 그대로다.
- **held-out 규칙:** 판정에서 본 실패를 보고 고치면 그 문항은 dev 로 옮기고 새 문항으로 채운다.
- **한계:** 판정자는 Claude 한 명이다. 묶음은 약 2MB(문항당 약 21KB)로 어림한다.

## 7. 접어 둔 라운드 (승자 모델로 다시 재기)

| 순서 | 라운드 | 9B 결과 | 다시 재는 법 |
|---|---|---|---|
| 1 | [`topic_answer_1104`](../topic_answer_1104/README.md) | 전체 없음 3>2 · 근거 없이 다룸 11>7 | `RAG_TOPIC_ANSWER=1` 로 HU40 답까지, §6 표와 비교. 못 넘으면 코드 삭제 |
| 2 | [`query_reform_1105`](../query_reform_1105/README.md) | 보호 1 −6.3%p | '거른 뒤 2~4편만 발동' 을 새 질문으로 사전 등록. 못 넘으면 코드 삭제 |
| 3 | [`topic_filter_1104`](../topic_filter_1104/README.md) · [`topic_split2_1104`](../topic_split2_1104/README.md) | 라벨 상한도 93/121 | §6.2 거르기 값으로 79 를 넘길 수 있는지 보고, 못 넘으면 `RAG_TOPIC_SPLIT` 삭제 |
| 4 | 문서당 1호출 판정 | 16GB 에서 미룸 | §6.2 뒤에 설계. 거르기 호출이 1번에서 15번으로 는다 |
| 5 | 컨텍스트 · 목록 칸 늘리기 | 4096 여유 약 470토큰이라 칸 10 제한 | `OLLAMA_CONTEXT_LENGTH` 8192, 그다음 `RAG_LIST_SLOTS`. 한 번에 하나만 |
| 6 | [`image_1104`](../image_1104/README.md) | X 10>6 · 새 정보 8<9 | `run.py` 의 `MODEL` 만 바꿔 같은 30장, 같은 기준. G2 미달이면 접는다. C 는 이미지를 못 받는다 |
| 7 | 재학습 | 9B 파인튜닝은 내용을 깎은 전례 | 위가 끝나고 형식 문제만 남을 때 작은 LoRA |

## 8. 사용자 결정 (도착 전)

1. **응답 시간 상한: 응답 중앙 120s 로 정함(사용자 결정 11-05).** 지금은 약 80s 다. 후보 탈락과 70B 생사를 가른다.
2. **FileVault · 자동 로그인.** 지금은 FileVault 켜짐 · 자동 로그인 없음이라, 재부팅이나 정전 뒤에는 사람이 로그인해야 봇이 돈다. 제안은 지금처럼 두는 것이다. 자동 복구를 원하면 FileVault 를 꺼야 한다.
3. **`com.yunsupark.chatbot`(포트 8081) 을 옮길지.** 별도 프로젝트이고 내용은 보지 않았다. 제안은 같이 옮기는 것이다.
4. **70B 후보.** `llama3.3` 은 이전 세대이고 글만 받는다. 제안은 §6.1 속도까지만 재 보는 것이다.

## 9. 옛 맥미니

§6 결과를 보고 정한다. 70B 를 채택하면 보조 모델 + 수집 서버로 남기는 쪽이 낫고(역할별 Ollama 주소 코드 필요), 30B 급 이하면 판매 쪽이다. 지우기 전에 `~/backups` 를 새 기기로 옮기고, 새 기기에서 2주 이상 탈 없이 돈 것을 확인한다.
