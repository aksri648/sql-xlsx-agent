from backend.langgraph.state import AnalystState


async def validation_node(state: AnalystState) -> AnalystState:
    return {**state, "error": None}