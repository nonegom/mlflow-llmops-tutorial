from typing import Annotated, Iterable, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph_module import State

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
            yield value["messages"][-1].content
