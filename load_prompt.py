from typing import Iterable 
from mlflow_module import load_prompts_by_version, load_prompts_by_alias
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph_module import State, get_llm


def prompt_chatbot(state: State, llm: ChatOpenAI):
    """LangGraph 노드: 누적 메시지와 추가 프롬프트를 기반으로 LLM을 호출한다."""
    # system 프롬프트를 가장 앞에 추가
    prompt = load_prompts_by_alias()
    prompt_str = prompt.template
    messages = [("system", prompt_str)] + state["messages"]
    print(messages)
    return  {"messages": [llm.invoke(messages)]}


def build_graph(llm: ChatOpenAI):
    """그래프를 구성하고 컴파일된 그래프를 반환한다."""
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", lambda s: prompt_chatbot(s, llm))
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    # 그래프 컴파일
    return graph_builder.compile()


def stream_answers(graph, question: str) -> Iterable[str]:
    """그래프를 실행하여 생성되는 메시지 텍스트를 순차적으로yield한다."""
    for event in graph.stream({"messages": [("user", question)]}):
        for value in event.values():
            yield value["messages"][-1].content


if __name__ =="__main__":
    llm = get_llm()
    graph = build_graph(llm)
    question = "가락시장 근처 맛집 3군데를 알려줘"
    prompt = load_prompts_by_alias()
    print(prompt.template)
    for text in stream_answers(graph, question):
        print(text)