from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
import os
import json

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)


async def response_formatter_node(state: AnalystState) -> AnalystState:
    question = state["question"]
    insights = state.get("insights", {})
    visualization = state.get("visualization", {})
    generated_sql = state.get("generated_sql", "")
    generated_pandas = state.get("generated_pandas", "")
    external_sources = state.get("external_sources", [])

    prompt = f"""Format the analysis response for the user.

Question: {question}
Insights: {json.dumps(insights)}
Visualization: {json.dumps(visualization)}
Generated SQL: {generated_sql}
Generated Pandas: {generated_pandas}
Sources: {external_sources}

Return JSON with:
- answer: natural language response
- insights: list of key insights
- chart: chart configuration
- generated_sql: the SQL query if any
- generated_pandas: the Pandas code if any
- sources: list of sources
- follow_up_questions: suggested follow-up questions"""

    response = await llm.ainvoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)

    try:
        formatted = json.loads(content)
    except:
        formatted = {"answer": "Analysis complete", "insights": [], "chart": None}

    return {
        **state,
        "response": {
            **formatted,
            "chart": visualization,
        }
    }