import mlflow

def set_mlflow_experiments(experiments_id="194958487408033668"):
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment(experiment_id=experiments_id)

    # langchain log를 할려면 autolog만 하면 된다.
    mlflow.langchain.autolog()
# default experiments log
set_mlflow_experiments()

def log_model(graph_model, run_name=None):
    mlflow.models.set_model(graph_model)
    with mlflow.start_run(run_name=run_name):
        logged_agent_info = mlflow.langchain.log_model(
            lc_model="simple_langgraph_agent.py",
            name="simple_model"  # graph workflow
        )
    return logged_agent_info


def load_model(model_uri):
    loaded_model = mlflow.langchain.load_model(model_uri)
    return loaded_model


def load_prompts_by_version(version=1):
    prompt = mlflow.genai.load_prompt(f"prompts:/sample-test/{version}")
    return prompt


def load_prompts_by_alias(alias='champion'):
    prompt = mlflow.genai.load_prompt(f"prompts:/sample-test@{alias}")
    return prompt
