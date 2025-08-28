from typing import Annotated, Iterable, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import argparse
import os


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

class State(TypedDict):
    # 메시지 정의(list type 이며 add_messages 함수를 사용하여 메시지를 추가)
    messages: Annotated[list, add_messages]

# 챗봇 함수 정의
def chatbot(state: State, llm: ChatOpenAI):
    """LangGraph 노드: 누적 메시지를 기반으로 LLM을 호출한다."""
    return {"messages": [llm.invoke(state["messages"])]}


###### STEP 3. 그래프(Graph) 정의, 노드 추가 ######
def build_graph(llm: ChatOpenAI):
    """그래프를 구성하고 컴파일된 그래프를 반환한다."""
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", lambda s: chatbot(s, llm))
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    # 그래프 컴파일
    return graph_builder.compile()

def stream_answers(graph, question: str) -> Iterable[str]:
    """그래프를 실행하여 생성되는 메시지 텍스트를 순차적으로yield한다."""
    for event in graph.stream({"messages": [("user", question)]}):
        for value in event.values():
            yield value["messages"][ -1 ].content


def main() -> None:
    parser = argparse.ArgumentParser(description="LangGraph 샘플 챗봇")
    parser.add_argument(
        "question",
        nargs="?",
        default="서울의 유명한 맛집 TOP 10 추천해줘",
        help="질문 프롬프트 (기본값 제공)",
    )
    args = parser.parse_args()

    llm = get_llm()
    graph = build_graph(llm)
    for text in stream_answers(graph, args.question):
        print(text)

if __name__ == "__main__":
    main()