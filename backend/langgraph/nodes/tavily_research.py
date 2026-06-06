from backend.langgraph.state import AnalystState
from langchain_groq import ChatGroq
from tavily import TavilyClient
import os

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=os.getenv("GROQ_API_KEY"),
)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


async def tavily_research_node(state: AnalystState) -> AnalystState:
    question = state["question"]

    try:
        context = tavily.search(question, max_results=5)
        sources = [item["url"] for item in context.get("results", [])]
        research_context = context.get("results", [])
    except:
        sources = []
        research_context = []

    return {
        **state,
        "tavily_context": research_context,
        "external_sources": sources,
    }