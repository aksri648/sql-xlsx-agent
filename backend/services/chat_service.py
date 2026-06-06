from backend.langgraph.graph import run_analyst
from backend.models.requests import ChatRequest
from backend.models.responses import ChatResponse


class ChatService:
    def __init__(self):
        pass

    async def process_question(self, request: ChatRequest) -> ChatResponse:
        return await run_analyst(request)