from mlflow_module import set_mlflow_experiments, log_model, load_model
from simple_langgraph_agent import build_graph
from langgraph_module import get_llm, stream_answers


# 등록한 모델을 사용하기

# loaded_model = mlflow.langchain.load_model(model_uri=model_uri)

if __name__ == '__main__':
    set_mlflow_experiments()
    print('mlflow experiments 설정 완료')
    
    llm = get_llm()
    graph = build_graph(llm)
    logged_agent_info = log_model(graph)
    
    model_uri = logged_agent_info.model_uri
    
    question = '가락시장 근처 맛집 3군데를 알려줘'
    loaded_model = load_model(model_uri)
    for text in stream_answers(loaded_model, question):
        print(text)