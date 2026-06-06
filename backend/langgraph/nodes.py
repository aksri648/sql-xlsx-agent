from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
import os
import json

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)


async def data_source_router_node(state: AnalystState) -> AnalystState:
    question = state["question"]

    prompt = f"""Analyze this question and determine if it should use uploaded files, a SQL database, or hybrid mode.

Question: {question}

Return JSON with source_type: "file", "database", or "hybrid"."""

    response = await llm.ainvoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)

    try:
        result = json.loads(content)
        source_type = result.get("source_type", "file")
    except:
        source_type = "file"

    return {**state, "source_type": source_type}


async def schema_discovery_node(state: AnalystState) -> AnalystState:
    return {**state, "schema_context": {}}


async def context_retrieval_node(state: AnalystState) -> AnalystState:
    return {**state, "retrieved_context": []}


async def question_understanding_node(state: AnalystState) -> AnalystState:
    question = state["question"]

    prompt = f"""Extract structured information from this question.

Question: {question}

Return JSON with:
- intent: what the user wants to accomplish
- metrics: list of metrics to calculate
- dimensions: list of dimensions to group by
- filters: list of filter conditions
- date_range: any time period mentioned"""

    response = await llm.ainvoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)

    try:
        result = json.loads(content)
    except:
        result = {"intent": question, "metrics": [], "dimensions": [], "filters": [], "date_range": ""}

    return {
        **state,
        "intent": result.get("intent", ""),
        "metrics": result.get("metrics", []),
        "dimensions": result.get("dimensions", []),
        "filters": result.get("filters", []),
        "date_range": result.get("date_range", ""),
    }


async def analysis_planner_node(state: AnalystState) -> AnalystState:
    question = state["question"]
    intent = state.get("intent", "")

    prompt = f"""Create an execution plan for this analysis question.

Question: {question}
Intent: {intent}

Return a JSON array of steps to execute the analysis."""

    response = await llm.ainvoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)

    try:
        plan = json.loads(content)
        if not isinstance(plan, list):
            plan = []
    except:
        plan = ["Analyze the data", "Generate insights"]

    return {**state, "analysis_plan": plan}