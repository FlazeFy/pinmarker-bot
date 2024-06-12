from fastapi import APIRouter, HTTPException
from services.modules.pin.pin_queries import get_all_pin

router_pin = APIRouter()

# GET Query
@router_pin.get("/api/v1/pin/{id}", response_model=dict)
async def get_all_pin_api(id: str):
    try:
        return await get_all_pin(type='api')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    