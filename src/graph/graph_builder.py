# Schemas
from .schemas import State
# LangGraph
from langgraph.graph import StateGraph
# Registry
from .registry import register_nodes
# Topology
from .topology import register_topology

def create_graph():
    graph_builder = StateGraph( State )
    register_nodes( graph_builder )
    register_topology( graph_builder )
    return graph_builder.compile()