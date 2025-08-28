from langgraph_sample import get_llm, build_graph, stream_answers
import mlflow


def set_mlflow_experiments():
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment(experiment_id="417156008591960350")

    # langchain log를 할려면 autolog만 하면 된다.
    mlflow.langchain.autolog()

if __name__ =="__main__":
    set_mlflow_experiments()
    question = "서울 가락시장역 근처 맛집 3개를 알려줘"
    llm = get_llm()
    graph = build_graph(llm)
    for text in stream_answers(graph, question):
        print(text)