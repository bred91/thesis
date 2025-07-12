from online_pipeline_models.models.chain_agent_react import ChainAgentReact
from online_pipeline_models.models.chain_multi_query import ChainMultiQuery
from online_pipeline_models.models.chain_simple import ChainSimple
from online_pipeline_models.models.graph_agent_react import GraphAgentReact
from online_pipeline_models.models.graph_agent_react_vanilla import GraphAgentReactVanilla

REGISTRY = {
    "simple": ChainSimple,
    "multi_query": ChainMultiQuery,
    "chain_agent_react": ChainAgentReact,
    "graph_agent_react": GraphAgentReact,                       # final model
    "graph_agent_react_vanilla": GraphAgentReactVanilla,        # Vanilla version of GraphAgentReact, for testing references
}

def get_chat_pipeline(name: str):
    try:
        return REGISTRY[name]()
    except KeyError:
        raise ValueError(f"Pipeline '{name}' non valida. Scegli tra {list(REGISTRY)})")