from fastapi import APIRouter, HTTPException
from services.modules.pin.pin_queries import get_all_pin, get_pin_by_category_query,get_all_pin_export_query

router_pin = APIRouter()

# GET Query
@router_pin.get("/api/v1/pin/{id}", response_model=dict)
async def get_all_pin_api(id: str):
    try:
        return await get_all_pin(userId=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin_export/{id}", response_model=dict)
async def get_all_pin_export_api(id: str):
    try:
        return await get_all_pin_export_query(userId=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin/{category}/{id}", response_model=dict)
# category can be multiple and separate by comma
# ex : cafe,restaurant
async def get_pin_by_category(category: str, id: str):
    try:
        return await get_pin_by_category_query(category=category, user_id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    