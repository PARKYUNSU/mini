# Chroma 빈틈 채우기 — BM25 에만 있는 논문 66편 (2026-11-01)

> 출발점: [`name_lookup_1101`](../name_lookup_1101/README.md) §7.3. 이름 찾기로 고른 논문 2편(DynamicRAG 2505.07233 · Block-Sphere 2605.19972)이 Chroma 에 청크가 없어 컨텍스트에 넣지 못했다. 전체를 세 보니 BM25 색인 7,797편 중 66편이 Chroma 에 없었다(커밋 080d9ca). 이 66편은 벡터 검색 · BM25 합집합 주입 · 이름 찾기 어느 경로로도 컨텍스트에 못 들어간다.
> 처리(§3)는 **쓰기 전에** 적었다. 운영 Chroma 쓰기는 사용자 승인 뒤에만 한다.

## 1. 목록 다시 만들기 — `find_gap.py` (읽기만) → `gap_before.jsonl`

- 처음에는 BM25 논문마다 서버에 `get(where={"paper_id": {"$in": 버전 후보}}, limit=1)` 를 했다. 앞쪽(`processed/`) 논문은 0.1초대였지만 대기열 JSONL 논문은 한 번에 4~7초가 걸렸고 서버 CPU 가 30~80% 였다. 남은 5,800편이면 몇 시간 부하라 2,000편(빠짐 7)에서 멈췄다.
- 대신 Chroma SQLite 를 **읽기 전용**(`immutable=1`, 잠금 없음 — `scripts/rebuild_chroma.py` 와 같은 방식)으로 열어 `arxiv_papers` 메타데이터 세그먼트의 paper_id 를 색인으로 한 번에 읽었다(94초, 서버를 거치지 않음). 저널 모드는 `delete`(WAL 아님)이고, 마지막 쓰기는 매일 수집(01:10)이며 그 뒤 쓰기는 없었다.
- BM25 에만 있는 후보 66편은 서버 get 으로 다시 확인했다: **66/66 없음**. 앞 2,000편 중 후보 7편은 서버 get 으로 센 7편과 같다.
- 결과: Chroma 청크 1,389,638 · 논문 7,731, BM25 7,797 → **BM25 에만 66편, Chroma 에만 0편**. 080d9ca 의 숫자와 같다.

## 2. 원인 — `classify.py` (읽기만) → `gap_causes.jsonl`

| 의심 | 결과 |
|---|---|
| 본문이 비었나 | **아니다.** 66편 모두 본문 2.1만~17.3만 자, 초록도 있다. 운영 청킹(`RagProcessor.chunk_markdown` + 품질 필터)에 넣으면 편당 44~478청크, 합 **12,297청크**가 나온다. |
| 10-13 · 10-14 Chroma 재구축 때 잃었나 | **아니다.** 10-13 사고 전 원본 백업(`backup/mini-chroma-old-20261013`)과 10-13 재구축본(`mini-chroma-rebuild`) 모두 66편 중 **0편**이다. 재구축 전부터 없었다. |
| 10-13 뒤에 들어온 논문인가 | **아니다.** 10-15 [`emb_cache_1015`](../emb_cache_1015/README.md) §6 에 이미 "BM25 7,103 · Chroma 7,037 → 66편"이 있다. 그 뒤 BM25 와 Chroma 가 똑같이 +694편 늘었다 → 10-15 이후 수집은 빠짐이 없다. 66편은 전부 3~5월 수집분이다. |
| 적재(임베딩)가 실패했나 | 묶음 A 는 그렇다(아래). B · C 는 기록이 모자라 확정하지 못했다. |

### 묶음

| 묶음 | 편수 | 청크 | 무엇 | 근거 |
|---|---|---|---|---|
| **A** | 40 | 7,829 | 2026-05-20 일일 수집 한 번 — 대기열 JSONL 704~743째 줄 연속(05-19 게재 cs.AI 최신 40편) 전부 | 그날 수집 로그는 남아 있지 않다(스케줄러 로그는 10-07부터). 같은 05-19 · 05-20 Phase35 심사관 로그(`.cron/phase35_curator_stdout.log`)에 `[Errno 28] No space left on device` 3회와 `sqlite3.OperationalError: unable to open database file` 2회가 있다. 디스크가 가득 찬 동안 JSONL 저장은 되고 Chroma 쓰기만 실패한 것으로 본다. |
| **B** | 7 | 1,261 | 3~4월 수집분. 04-04 백업(`chroma_db_backup_20260404_1442`)에는 **있었는데** 10-13 원본에는 없다 | 04-04 ~ 10-13 사이 DB 교체(재구축이나 경로 이동) 때 빠졌다. 그 교체 기록은 찾지 못했다. |
| **C** | 19 | 3,207 | 3~4월 수집분(`processed/` 16편 · 대기열 3편). 남아 있는 어느 DB 에도 없다 | 파일당 1편 꼴로 흩어져 있다(2,585편 파일에서 12편 등). 9편은 4월 타깃 수집 로그(`logs/targeted_batch_crawl.log`)에 적재 단계가 오류 없이 찍혔는데 10-13 원본에 없다 → B 와 같은 유실로 추정하지만 확정하지 못했다. 나머지 10편은 로그가 없다. 2편(2412.11453 · 2504.00035)은 10-07 검색 평가 로그에도 "Chroma 에 없음"으로 나온다. |

### 왜 그대로 남았나 (공통)

- 수집 경로 다섯 곳(`pipelines.ingest.main` · `hf_daily` · `apps.backfill.ingest_classics` · `run_targeted_batch_crawl` · `phase35_auto_curator`)이 모두 **JSONL 에 먼저 저장하고** Chroma 에 넣는다. Chroma 가 실패하면 로그만 찍고 넘어간다.
- 다음 수집은 JSONL 에 있는 논문을 "이미 저장됨"으로 건너뛴다. 그래서 다시 넣지 않는다. 기존 수집 스크립트로는 이미 JSONL 에 있는 논문을 다시 적재할 수 없다.
- `pipelines.ingest.main` 은 Chroma 실패가 있어도 성공 마커(`arxiv_pipeline_ok_*.marker`)를 쓴다. 텔레그램 알림의 "N개 논문 수집 및 RAG 적재 완료"의 N 은 JSONL 저장 수다.
- `ingest_watchdog`(10-12 도입)는 오늘자 성공 마커 · 스케줄러 프로세스 · 디스크 여유만 본다. JSONL 과 Chroma 를 맞대 보지 않는다. 게다가 66편은 감시를 넣기 전(3~5월)에 생겼다.

### 66편

| 묶음 | paper_id | 제목 | JSONL 첫 위치 | 예상 청크 |
|---|---|---|---|---|
| A | 2605.19940 | Robotics-Inspired Guardrails for Foundation Models in Soc… | `crawled_papers.jsonl:743` | 403 |
| A | 2605.19943 | Probabilistic Tiny Recursive Model | `crawled_papers.jsonl:742` | 138 |
| A | 2605.19944 | A Measure-Theoretic Analysis of Reasoning: Structural Gen… | `crawled_papers.jsonl:741` | 268 |
| A | 2605.19945 | GEM: GPU-Variability-Aware Expert to GPU Mapping for MoE … | `crawled_papers.jsonl:740` | 230 |
| A | 2605.19957 | World-Ego Modeling for Long-Horizon Evolution in Hybrid E… | `crawled_papers.jsonl:739` | 232 |
| A | 2605.19966 | Detecting Fluent Optimization-Based Adversarial Prompts v… | `crawled_papers.jsonl:738` | 64 |
| A | 2605.19972 | Block-Sphere Vector Quantization | `crawled_papers.jsonl:737` | 325 |
| A | 2605.19975 | Learning with Foresight: Enhancing Neural Routing Policy … | `crawled_papers.jsonl:736` | 175 |
| A | 2605.19988 | A Case for Agentic Tuning: From Documentation to Action i… | `crawled_papers.jsonl:735` | 210 |
| A | 2605.19999 | LLM Benchmark Datasets Should Be Contamination-Resistant | `crawled_papers.jsonl:734` | 196 |
| A | 2605.20006 | GeoX: Mastering Geospatial Reasoning Through Self-Play an… | `crawled_papers.jsonl:733` | 241 |
| A | 2605.20009 | Training Neural Networks with Optimal Double-Bayesian Lea… | `crawled_papers.jsonl:732` | 149 |
| A | 2605.20023 | When Skills Don't Help: A Negative Result on Procedural K… | `crawled_papers.jsonl:731` | 63 |
| A | 2605.20025 | AutoResearchClaw: Self-Reinforcing Autonomous Research wi… | `crawled_papers.jsonl:730` | 228 |
| A | 2605.20037 | When Critics Disagree: Adaptive Reward Poisoning Attacks … | `crawled_papers.jsonl:729` | 64 |
| A | 2605.20049 | Does Code Cleanliness Affect Coding Agents? A Controlled … | `crawled_papers.jsonl:728` | 126 |
| A | 2605.20052 | PromptRad: Knowledge-Enhanced Multi-Label Prompt-Tuning f… | `crawled_papers.jsonl:727` | 163 |
| A | 2605.20055 | Towards LLM-Assisted Architecture Recovery for Real-World… | `crawled_papers.jsonl:726` | 121 |
| A | 2605.20072 | Probing Embodied LLMs: When Higher Observation Fidelity H… | `crawled_papers.jsonl:725` | 91 |
| A | 2605.20075 | CopT: Contrastive On-Policy Thinking with Continuous Spac… | `crawled_papers.jsonl:724` | 186 |
| A | 2605.20079 | Probability-Conserving Flow Guidance | `crawled_papers.jsonl:723` | 184 |
| A | 2605.20082 | VL-DPO: Vision-Language-Guided Finetuning for Preference-… | `crawled_papers.jsonl:722` | 103 |
| A | 2605.20084 | BalanceRAG: Joint Risk Calibration for Cascaded Retrieval… | `crawled_papers.jsonl:721` | 273 |
| A | 2605.20086 | What Do Evolutionary Coding Agents Evolve? | `crawled_papers.jsonl:720` | 252 |
| A | 2605.20087 | ThoughtTrace: Understanding User Thoughts in Real-World L… | `crawled_papers.jsonl:719` | 478 |
| A | 2605.20088 | INSHAPE: Instance-Level Shapelets for Interpretable Time-… | `crawled_papers.jsonl:718` | 254 |
| A | 2605.20098 | Neurosymbolic Learning for Inference-Time Argumentation | `crawled_papers.jsonl:717` | 199 |
| A | 2605.20104 | Draft Less, Retrieve More: Hybrid Tree Construction for S… | `crawled_papers.jsonl:716` | 354 |
| A | 2605.20107 | Beyond Isotropy in JEPAs: Hamiltonian Geometry and Symple… | `crawled_papers.jsonl:715` | 376 |
| A | 2605.20108 | k-Inductive Neural Barrier Certificates for Unknown Nonli… | `crawled_papers.jsonl:714` | 132 |
| A | 2605.20119 | Toto 2.0: Time Series Forecasting Enters the Scaling Era | `crawled_papers.jsonl:713` | 195 |
| A | 2605.20120 | Using Aristotle API for AI-Assisted Theorem Proving in Le… | `crawled_papers.jsonl:712` | 44 |
| A | 2605.20127 | Beyond Prediction Accuracy: Target-Space Recovery Profile… | `crawled_papers.jsonl:711` | 55 |
| A | 2605.20149 | Less Back-and-Forth: A Comparative Study of Structured Pr… | `crawled_papers.jsonl:710` | 77 |
| A | 2605.20158 | Rethinking Visual Attribution for Chest X-ray Reasoning i… | `crawled_papers.jsonl:709` | 273 |
| A | 2605.20164 | Not Every Rubric Teaches Equally: Policy-Aware Rubric Rew… | `crawled_papers.jsonl:708` | 210 |
| A | 2605.20167 | HaorFloodAlert: Deseasonalized ML Ensemble for 72-Hour Fl… | `crawled_papers.jsonl:707` | 91 |
| A | 2605.20172 | Long-term Power Grid Planning via Answer Set Programming | `crawled_papers.jsonl:706` | 149 |
| A | 2605.20173 | A Methodology for Selecting and Composing Runtime Archite… | `crawled_papers.jsonl:705` | 202 |
| A | 2605.20182 | Atoms of Thought: Universal EEG Representation Learning w… | `crawled_papers.jsonl:704` | 255 |
| B | 2404.00172 | Universal Bovine Identification via Depth Data and Deep M… | `processed/crawled_papers_1775560679.jsonl:97` | 244 |
| B | 2406.18420 | Mixture of Experts in a Mixture of RL settings | `processed/crawled_papers_1775560679.jsonl:518` | 224 |
| B | 2412.14170 | E-CAR: Efficient Continuous Autoregressive Image Generati… | `processed/crawled_papers_1775064075.jsonl:144` | 146 |
| B | 2412.16381 | VerSe: Integrating Multiple Queries as Prompts for Versat… | `processed/crawled_papers_1774430316.jsonl:79` | 121 |
| B | 2412.17744 | RepoTransBench: A Real-World Multilingual Benchmark for R… | `processed/crawled_papers_1774414297.jsonl:917` | 211 |
| B | 2604.01170 | Online Reasoning Calibration: Test-Time Training Enables … | `processed/crawled_papers_1775560679.jsonl:302` | 191 |
| B | 2604.02118 | LLM-as-a-Judge for Time Series Explanations | `processed/crawled_papers_1775560679.jsonl:712` | 124 |
| C | 2311.04177 | Enhancing LLM Intelligence with ARM-RAG: Auxiliary Ration… | `processed/crawled_papers_1775560679.jsonl:2417` | 93 |
| C | 2402.01769 | Redefining "Hallucination" in LLMs: Towards a psychology-… | `processed/crawled_papers_1776063800.jsonl:5` | 94 |
| C | 2407.19643 | Prometheus Chatbot: Knowledge Graph Collaborative Large L… | `crawled_papers.jsonl:92` | 77 |
| C | 2412.08463 | IRL for Restless Multi-Armed Bandits with Applications in… | `processed/crawled_papers_1775560679.jsonl:1755` | 98 |
| C | 2412.10047 | Large Action Models: From Inception to Implementation | `processed/crawled_papers_1775560679.jsonl:1535` | 374 |
| C | 2412.11453 | ACE-$M^3$: Automatic Capability Evaluator for Multimodal … | `processed/crawled_papers_1775560679.jsonl:1312` | 244 |
| C | 2412.13147 | Are Your LLMs Capable of Stable Reasoning? | `processed/crawled_papers_1775560679.jsonl:1085` | 294 |
| C | 2503.21843 | CMD-HAR: Cross-Modal Disentanglement for Wearable Human A… | `processed/crawled_papers_1775560679.jsonl:2185` | 123 |
| C | 2504.00035 | Is Your Writing Being Mimicked by AI? Unveiling Imitation… | `processed/crawled_papers_1775560679.jsonl:1952` | 169 |
| C | 2505.07233 | DynamicRAG: Leveraging Outputs of Large Language Model as… | `processed/crawled_papers_1775661446.jsonl:1` | 221 |
| C | 2506.15513 | RePCS: Diagnosing Data Memorization in LLM-Powered Retrie… | `processed/crawled_papers_1775640340.jsonl:1` | 99 |
| C | 2511.03728 | Efficient On-Device Agents via Adaptive Context Management | `crawled_papers.jsonl:334` | 114 |
| C | 2511.15370 | The Empowerment of Science of Science by Large Language M… | `processed/crawled_papers_1776058321.jsonl:5` | 120 |
| C | 2603.24511 | Claudini: Autoresearch Discovers State-of-the-Art Adversa… | `processed/crawled_papers_1776051041.jsonl:4` | 152 |
| C | 2603.25075 | Sparse Visual Thought Circuits in Vision-Language Models | `processed/crawled_papers_1776069997.jsonl:3` | 173 |
| C | 2603.26076 | Semi-Automated Knowledge Engineering and Process Mapping … | `processed/crawled_papers_1776055914.jsonl:5` | 98 |
| C | 2604.02545 | Competency Questions as Executable Plans: a Controlled RA… | `processed/crawled_papers_1775563927.jsonl:1` | 180 |
| C | 2604.06086 | LAG-XAI: A Lie-Inspired Affine Geometric Framework for In… | `processed/crawled_papers_1776061452.jsonl:5` | 240 |
| C | 2604.27977 | D3-Gym: Constructing Real-World Verifiable Environments f… | `crawled_papers.jsonl:566` | 244 |

(JSONL 위치는 `raw_data_queue/` 아래. 9편은 JSONL 여러 곳에 있다 — `gap_before.jsonl` 의 `where`.)

## 3. 처리 — 사용자 승인 뒤에만

- `fill_gap.py`: 66편마다 JSONL 레코드(BM25 색인과 같은 첫 줄)를 읽어 `RagProcessor.add_paper` 를 `chroma_write_lock()` 안에서 부른다. `hf_daily` · `ingest_classics` 와 같은 호출이다(청킹 · 품질 필터 · 같은 임베딩 · 결정적 청크 ID · upsert). 새 임베딩 코드는 없다. 이미 Chroma 에 있는 논문은 건너뛴다.
- 본문은 JSONL `content` 다. 처음 수집 때 넣은 마크다운에 수식 구분자 정리(`enrich_text_for_llm_math`: `\(..\)` → `$..$`, `\[..\]` → `$$..$$`)만 더한 것이고, 옛 JSONL 재적재 스크립트들(`scripts/legacy/rebuild_chroma_*.py`)도 같은 필드를 썼다. PDF 를 다시 받지 않는다.
- 쓰기량: **66편 · 12,297청크**(컬렉션 1,389,638 → 1,401,935 예상).
- 순서: 1편(2505.07233 DynamicRAG)을 먼저 넣고 get · 벡터 검색으로 확인한 뒤 나머지 65편.
- 쓰기 전에 `pgrep -fl "eval_e2e_ko[.]py|weekly_check[.]sh"` 가 비었는지 본다. 매일 01:00 수집과 일요일 04:00 주간 점검 시간은 피한다. 쓰기 잠금은 편마다 잡으므로 잠금 동안(편당 수 초) 봇 검색은 JSONL 로 넘어간다.
- `.env` 변경 · 봇 재시작은 없다. 임베딩 캐시(`RAG_EMB_CACHE=1`)는 행 수가 바뀌면 '불완전'으로 보고, 캐시에 없는 논문(채운 66편)만 Chroma 에서 직접 가져온다. 오늘 밤 01:00 수집 뒤 캐시를 재생성할 때 들어간다.

## 4. 판정 (쓰기 전 고정)

| 지표 | 기준 |
|---|---|
| **주:** 다시 센 "BM25 에만 있는 논문" | 0편(못 채운 것은 이유와 함께 적는다) |
| 넣은 청크 합 | 12,297(청킹 예상과 같음) · "Chroma 에만 있는 논문" 0 유지 |
| 확인 | DynamicRAG(2505.07233) · Block-Sphere(2605.19972) 제목으로 벡터 검색하면 상위에 나온다 |

## 5. 결과

(채운 뒤에 쓴다.)

## 파일

- `find_gap.py` — 목록(읽기만) · `gap_before.jsonl` — 66편(JSONL 위치 · 길이)
- `classify.py` — 원인(옛 DB 대조 · 로그 · 청킹 수, 읽기만) · `gap_causes.jsonl`
- `fill_gap.py` — 채우기(승인 뒤) · `fill_result.jsonl` — 편마다 넣은 청크 수
