from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import uuid

from backend.models.requests import ChatRequest
from backend.models.responses import ChatResponse
from backend.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ChatService()


@router.post("")
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = await chat_service.process_question(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    async def event_generator():
        try:
            response = await chat_service.process_question(request)

            yield f"data: {json.dumps({'type': 'start'})}\n\n"

            yield f"data: {json.dumps({'type': 'answer', 'content': response.answer})}\n\n"

            for insight in response.insights:
                yield f"data: {json.dumps({'type': 'insight', 'content': insight})}\n\n"

            if response.chart:
                yield f"data: {json.dumps({'type': 'chart', 'content': response.chart.dict()})}\n\n"

            if response.generated_sql:
                yield f"data: {json.dumps({'type': 'sql', 'content': response.generated_sql})}\n\n"

            if response.generated_pandas:
                yield f"data: {json.dumps({'type': 'pandas', 'content': response.generated_pandas})}\n\n"

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )