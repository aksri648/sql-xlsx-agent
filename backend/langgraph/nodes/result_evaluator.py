from backend.langgraph.state import AnalystState


async def result_evaluator_node(state: AnalystState) -> AnalystState:
    results = state.get("results", {})
    needs_external = len(results) == 0

    return {
        **state,
        "needs_external_research": needs_external,
    }