from simple_langgraph_agent import get_llm, build_graph, stream_answers
from mlflow_module import set_mlflow_experiments

if __name__ =="__main__":
    set_mlflow_experiments()
    question = "서울 가락시장역 근처 맛집 3개를 알려줘"
    llm = get_llm()
    graph = build_graph(llm)
    for text in stream_answers(graph, question):
        print(text)