from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
import os
import json

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)


async def visualization_node(state: AnalystState) -> AnalystState:
    question = state["question"]
    results = state.get("results", {})

    prompt = f"""Choose the best visualization for this analysis.

Question: {question}
Results: {json.dumps(results)}

Rules:
- Time Series → Line Chart
- Comparison → Bar Chart
- Distribution → Histogram
- Correlation → Scatter Plot
- Composition → Pie Chart

Return JSON with chart_type, x_axis, y_axis."""

    response = await llm.ainvoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)

    try:
        visualization = json.loads(content)
    except:
        visualization = {"chart_type": "bar", "x_axis": "", "y_axis": ""}

    return {**state, "visualization": visualization}