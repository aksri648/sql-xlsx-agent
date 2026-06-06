from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
import os
import json

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)


async def schema_discovery_node(state: AnalystState) -> AnalystState:
    question = state["question"]

    prompt = f"""Identify the schema or data structure needed to answer this question.

Question: {question}

Return JSON with schema_context describing the data needed."""
    response = await llm.ainvoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)

    try:
        result = json.loads(content)
        schema_context = result.get("schema_context", {})
    except:
        schema_context = {}

    return {**state, "schema_context": schema_context}