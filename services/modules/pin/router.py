from fastapi import APIRouter, HTTPException, Request
from services.modules.pin.pin_queries import get_all_pin, get_pin_by_category_query,get_all_pin_export_query,get_global_list_query,get_nearest_pin_query

router_pin = APIRouter()

# For Telegram, Web, and Mobile
# GET Query
@router_pin.get("/api/v1/pin/{id}", response_model=dict)
async def get_all_pin_api(id: str):
    try:
        return await get_all_pin(userId=id, platform='telegram')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin_export/{id}", response_model=dict)
async def get_all_pin_export_api(id: str):
    try:
        return await get_all_pin_export_query(userId=id, platform='telegram')
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
    
@router_pin.get("/api/v1/pin_global/{search}", response_model=dict)
async def get_global_list_api(search: str):
    try:
        return await get_global_list_query(search=search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.post("/api/v1/pin/nearest/{lat}/{long}", response_model=dict)
async def get_nearest_pin_api(lat: str, long:str, request : Request):
    try:
        data = await request.json()
        return await get_nearest_pin_query(lat=lat, long=long, userid=data.get('id'), max_dis=data.get('max_distance'), limit=data.get('limit'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# For Discord
@router_pin.get("/api/v2/pin", response_model=dict)
async def get_all_pin_api():
    try:
        return await get_all_pin(userId=None, platform='discord')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v2/pin_export", response_model=dict)
async def get_all_pin_export_api():
    try:
        return await get_all_pin_export_query(userId=None, platform='discord')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    