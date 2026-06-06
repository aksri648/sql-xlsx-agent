from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from typing import Literal

from backend.langgraph.state import AnalystState
from backend.langgraph.nodes import (
    data_source_router_node,
    schema_discovery_node,
    context_retrieval_node,
    question_understanding_node,
    analysis_planner_node,
    sql_agent_node,
    pandas_agent_node,
    validation_node,
    execution_node,
    result_evaluator_node,
    tavily_research_node,
    context_merger_node,
    insight_node,
    visualization_node,
    response_formatter_node,
)
from backend.models.requests import ChatRequest
from backend.models.responses import ChatResponse
import os

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)

memory = MemorySaver()

workflow = StateGraph(AnalystState)

workflow.add_node("data_source_router", data_source_router_node)
workflow.add_node("schema_discovery", schema_discovery_node)
workflow.add_node("context_retrieval", context_retrieval_node)
workflow.add_node("question_understanding", question_understanding_node)
workflow.add_node("analysis_planner", analysis_planner_node)
workflow.add_node("sql_agent", sql_agent_node)
workflow.add_node("pandas_agent", pandas_agent_node)
workflow.add_node("validation", validation_node)
workflow.add_node("execution", execution_node)
workflow.add_node("result_evaluator", result_evaluator_node)
workflow.add_node("tavily_research", tavily_research_node)
workflow.add_node("context_merger", context_merger_node)
workflow.add_node("insight", insight_node)
workflow.add_node("visualization", visualization_node)
workflow.add_node("response_formatter", response_formatter_node)


def route_source(state: AnalystState) -> Literal["sql_agent", "pandas_agent"]:
    if state.get("source_type") == "database":
        return "sql_agent"
    return "pandas_agent"


workflow.add_edge(START, "data_source_router")
workflow.add_edge("data_source_router", "schema_discovery")
workflow.add_edge("schema_discovery", "context_retrieval")
workflow.add_edge("context_retrieval", "question_understanding")
workflow.add_edge("question_understanding", "analysis_planner")
workflow.add_edge("analysis_planner", "validation")
workflow.add_edge("validation", "execution")
workflow.add_edge("execution", "result_evaluator")

workflow.add_conditional_edges(
    "result_evaluator",
    lambda state: "tavily_research" if state.get("needs_external_research") else "insight",
    {
        "tavily_research": "tavily_research",
        "insight": "insight",
    }
)

workflow.add_edge("tavily_research", "context_merger")
workflow.add_edge("context_merger", "insight")
workflow.add_edge("insight", "visualization")
workflow.add_edge("visualization", "response_formatter")
workflow.add_edge("response_formatter", END)

graph = workflow.compile(checkpointer=memory)


def run_analyst(request: ChatRequest) -> ChatResponse:
    initial_state = {
        "question": request.question,
        "session_id": request.session_id or "default",
    }

    result = graph.invoke(initial_state, config={"configurable": {"thread_id": request.session_id}})

    return ChatResponse(
        answer=result.get("response", {}).get("answer", "No answer generated"),
        insights=result.get("response", {}).get("insights", []),
        chart=result.get("response", {}).get("chart"),
        generated_sql=result.get("generated_sql"),
        generated_pandas=result.get("generated_pandas"),
        sources=result.get("response", {}).get("sources", []),
        follow_up_questions=result.get("response", {}).get("follow_up_questions", []),
        session_id=result.get("session_id", "default"),
    )