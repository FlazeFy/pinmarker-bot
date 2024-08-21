from fastapi import APIRouter, HTTPException
from services.modules.stats.stats_queries import get_dashboard
from services.modules.stats.template import get_total_item_by_context

router_stats = APIRouter()

# GET Query
@router_stats.get("/api/v1/stats/dashboard/{id}/{role}", response_model=dict)
async def get_dashboard_route(id: str, role:str):
    try:
        return await get_dashboard(userId=id, role=role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router_stats.get("/api/v1/stats/total_pin_by_category/{id}", response_model=dict)
async def get_total_pin_by_category(id: str):
    try:
        data = await get_total_item_by_context(tableName="pin", join=None, targetColumn="pin_category", userId=id)
        if len(data) != 0:
            data_list = [dict(row._mapping) for row in data]
            return {
                "data": data_list,
                "message": "Stats found",
                "count": len(data)
            }
        else:
            return {
                "message": "No Stats found",
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_stats.get("/api/v1/stats/total_visit_by_category/{id}", response_model=dict)
async def get_total_visit_by_category(id: str):
    try:
        data = await get_total_item_by_context(tableName="visit", join="pin on pin.id = visit.pin_id", targetColumn="pin_category", userId=id)
        if len(data) != 0:
            data_list = [dict(row._mapping) for row in data]
            return {
                "data": data_list,
                "message": "Stats found",
                "count": len(data)
            }
        else:
            return {
                "message": "No Stats found",
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_stats.get("/api/v1/stats/total_gallery_by_pin/{id}", response_model=dict)
async def get_total_gallery_by_pin(id: str):
    try:
        data = await get_total_item_by_context(tableName="gallery", join="pin on pin.id = gallery.pin_id", targetColumn="pin_name", userId=id)
        if len(data) != 0:
            data_list = [dict(row._mapping) for row in data]
            return {
                "data": data_list,
                "message": "Stats found",
                "count": len(data)
            }
        else:
            return {
                "message": "No Stats found",
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    