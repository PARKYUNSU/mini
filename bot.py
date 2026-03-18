#!/usr/bin/env python3
"""
[Legacy] 단순 RAG 테스트용 봇
- Chroma DB 유사도 검색 → Ollama(Qwen)로 답변 생성
- 메인 봇은 agent_bot.py (RAG + Agent 통합). 24시간 구동 시 agent_bot만 사용.
"""

import os
from functools import lru_cache

# Ollama URL (ChatOllama import 전에 설정)
os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import telebot

load_dotenv()

# 환경 변수 (RAG_BOT_TOKEN 우선, 없으면 TELEGRAM_TOKEN)
TELEGRAM_TOKEN = os.getenv("RAG_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
ALLOWED_CHAT_ID = os.getenv("ALLOWED_CHAT_ID")
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "arxiv_papers"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = os.getenv("LOCAL_LLM_MODEL", "qwen3.5:9b")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5  # 검색할 문서 수

SYSTEM_PROMPT = """오직 다음 제공된 문서만을 바탕으로 질문에 대답해. 문서에 없는 내용은 지어내지 마. 답을 모르면 "문서에 해당 정보가 없습니다."라고 해."""


@lru_cache(maxsize=1)
def get_chroma_collection():
    """Chroma DB 컬렉션 반환 (모듈 로딩 시 1회 캐싱)"""
    embedding_fn = SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL,
        device="cpu",
        normalize_embeddings=True,
    )
    client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH,
        settings=Settings(anonymized_telemetry=False),
    )
    return client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
    )


def rag_query(question: str) -> str:
    """RAG: Chroma 검색 → Ollama 답변"""
    collection = get_chroma_collection()
    results = collection.query(
        query_texts=[question],
        n_results=TOP_K,
        include=["documents", "metadatas"],
    )

    docs = results["documents"][0] if results["documents"] else []
    if not docs:
        return "관련 문서를 찾지 못했습니다."

    context = "\n\n---\n\n".join(docs)

    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.1,
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"[참고 문서]\n{context}\n\n[질문]\n{question}"),
    ]
    response = llm.invoke(messages)
    return response.content


def main():
    if not TELEGRAM_TOKEN or not ALLOWED_CHAT_ID:
        print("❌ .env에 RAG_BOT_TOKEN(또는 TELEGRAM_TOKEN), ALLOWED_CHAT_ID를 설정하세요.")
        return

    allowed_ids = [aid.strip() for aid in ALLOWED_CHAT_ID.split(",")]
    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    @bot.message_handler(func=lambda m: True)
    def handle_message(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(
                message,
                f"접근 권한이 없는 사용자입니다.\n\n"
                f"당신의 Chat ID: `{chat_id}`\n"
                f".env의 ALLOWED_CHAT_ID에 이 값을 추가하세요.",
                parse_mode="Markdown",
            )
            return

        question = message.text.strip()
        if not question:
            bot.reply_to(message, "질문을 입력해 주세요.")
            return

        try:
            status_msg = bot.send_message(
                chat_id,
                "🔍 지식 베이스를 검색 중입니다...",
            )
            answer = rag_query(question)

            if len(answer) > 4000:
                answer = answer[:3997] + "..."

            bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_msg.message_id,
                text=answer,
            )
        except Exception as e:
            print(f"❌ 오류: {e}")
            try:
                bot.send_message(chat_id, "서버 오류가 발생했습니다.")
            except Exception:
                pass

    print("🤖 봇 시작 (Ctrl+C로 종료)")
    bot.remove_webhook()  # 웹훅 해제 (409 충돌 방지)
    bot.infinity_polling()


if __name__ == "__main__":
    main()
