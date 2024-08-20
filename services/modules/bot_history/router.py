from fastapi import APIRouter, HTTPException
from services.modules.bot_history.queries import get_bot_history

router_bot_history = APIRouter()

# GET Query
@router_bot_history.get("/api/v1/bot_history/{tele_id}", response_model=dict)
async def get_bot_history_api(tele_id: str):
    try:
        return await get_bot_history(tele_id=tele_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))