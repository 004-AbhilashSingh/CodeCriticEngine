from fastapi import APIRouter, Query, Body
from starlette.responses import JSONResponse

from src.Workflows.PrReviewWorkFlow import PrReviewWorkFlow
from src.services.CodeReviewService import CodeReviewService
from src.services.FormattingService import FormattingService

router = APIRouter(prefix="/llm")

@router.get("/test")
async def test_llm(text:str = Query(...)):
    service = CodeReviewService()
    response = service.test_llm(text)
    return JSONResponse(content=response.content, status_code=200)

@router.post("/review-code")
async def review_code(body: dict = Body(...)):
    code = body.get("code")
    service = CodeReviewService()
    response = service.review_code(code)
    response = FormattingService.convert_to_json(response.content)
    return JSONResponse(content=response, status_code=200)

@router.post("/review-pull-request")
async def review_pull_request(body: dict = Body(...)):
    diff = body.get("diff")
    workflow = PrReviewWorkFlow()
    response = workflow.engine.invoke({"diff": diff})
    response = FormattingService.convert_to_json(response['review'])
    return JSONResponse(content={"review":response}, status_code=200)