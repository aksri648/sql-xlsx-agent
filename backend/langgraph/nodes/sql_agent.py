from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
import os
import json

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)


async def sql_agent_node(state: AnalystState) -> AnalystState:
    question = state["question"]
    schema_context = state.get("schema_context", {})
    metrics = state.get("metrics", [])
    dimensions = state.get("dimensions", [])
    filters = state.get("filters", [])

    prompt = f"""Generate an optimized SQL query based on the question.

Question: {question}
Schema: {json.dumps(schema_context)}
Metrics: {metrics}
Dimensions: {dimensions}
Filters: {json.dumps(filters)}

Rules:
- Read-only SELECT queries only
- ANSI SQL compliant
- No SELECT *
- Use aliases
- Use aggregation in SQL
- Use LIMIT when appropriate
- Use efficient joins
- Use schema context only

Forbidden: INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, MERGE, EXECUTE

Return JSON with sql field containing the query."""

    response = await llm.ainvoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)

    try:
        result = json.loads(content)
        sql = result.get("sql", "SELECT 1")
    except:
        sql = "SELECT 1"

    return {**state, "generated_sql": sql}