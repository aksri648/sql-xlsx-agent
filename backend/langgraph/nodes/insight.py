from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
import os
import json

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)


async def insight_node(state: AnalystState) -> AnalystState:
    question = state["question"]
    results = state.get("results", {})
    tavily_context = state.get("tavily_context", [])

    prompt = f"""Generate insights from the analysis results.

Question: {question}
Results: {json.dumps(results)}
External Context: {json.dumps(tavily_context)}

Generate:
- Executive Summary
- Key Findings
- Trends
- Anomalies
- Recommendations

Style: Business-focused, concise, actionable, professional.

Return JSON with insight fields."""

    response = await llm.ainvoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)

    try:
        insights = json.loads(content)
    except:
        insights = {"summary": "Analysis complete", "findings": [], "recommendations": []}

    return {**state, "insights": insights}