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