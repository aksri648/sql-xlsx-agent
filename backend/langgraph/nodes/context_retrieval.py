from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
import os
import json

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)


async def context_retrieval_node(state: AnalystState) -> AnalystState:
    question = state["question"]
    schema_context = state.get("schema_context", {})

    prompt = f"""Retrieve relevant context for this analysis question.

Question: {question}
Schema: {json.dumps(schema_context)}

Return JSON with retrieved_context containing relevant context chunks."""
    response = await llm.ainvoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)

    try:
        result = json.loads(content)
        retrieved_context = result.get("retrieved_context", [])
    except:
        retrieved_context = []

    return {**state, "retrieved_context": retrieved_context}
