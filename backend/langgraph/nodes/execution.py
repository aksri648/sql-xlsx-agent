from backend.langgraph.state import AnalystState


async def execution_node(state: AnalystState) -> AnalystState:
    return {**state, "results": {}}