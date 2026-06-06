from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
import os
import json

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)


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