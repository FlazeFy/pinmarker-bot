from fastapi import APIRouter, HTTPException, Request
from services.modules.feedback.command import post_feedback

router_feedback = APIRouter()

# POST Command
@router_feedback.post("/api/v1/feedback", response_model=dict)
async def post_feedback_api(request : Request):
    try:
        data = await request.json()
        return await post_feedback(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))