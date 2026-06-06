from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
import os
import json

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)


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