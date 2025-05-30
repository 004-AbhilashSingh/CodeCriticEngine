from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from src.services.CodeReviewService import CodeReviewService

router = APIRouter(prefix="/llm")

@router.get("/test")
async def test_llm(text:str = Query(...)):
    service = CodeReviewService()
    response = service.test_llm(text)
    return JSONResponse(content=response.content, status_code=200)