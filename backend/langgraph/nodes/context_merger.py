from backend.langgraph.state import AnalystState


async def context_merger_node(state: AnalystState) -> AnalystState:
    return {**state}