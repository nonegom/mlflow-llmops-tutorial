
from typing import Annotated, Iterable, TypedDict
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

class State(TypedDict):
    # 메시지 정의(list type 이며 add_messages 함수를 사용하여 메시지를 추가)
    messages: Annotated[list, add_messages]


def get_llm() -> ChatOpenAI:
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY가 설정되어 있지 않습니다. .env 또는 환경변수를 확인하세요."
        )

    target_llm = os.environ.get("TARGET_LLM", "gpt-4.1-mini")
    try:
        temperature = float(os.environ.get("OPENAI_TEMPERATURE", "0"))
    except ValueError:
        temperature = 0.0

    return ChatOpenAI(model=target_llm, api_key=api_key, temperature=temperature)
