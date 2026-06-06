from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
import os
import json

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)


async def pandas_agent_node(state: AnalystState) -> AnalystState:
    question = state["question"]
    schema_context = state.get("schema_context", {})
    metrics = state.get("metrics", [])
    dimensions = state.get("dimensions", [])

    prompt = f"""Generate Pandas operations based on the question.

Question: {question}
Schema: {json.dumps(schema_context)}
Metrics: {metrics}
Dimensions: {dimensions}

Rules:
- Use only provided DataFrames
- No filesystem access
- No subprocess
- No shell execution
- No unsafe imports
- Return DataFrame operations

Return JSON with pandas_code field containing the code."""

    response = await llm.ainvoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)

    try:
        result = json.loads(content)
        pandas_code = result.get("pandas_code", "df")
    except:
        pandas_code = "df"

    return {**state, "generated_pandas": pandas_code}