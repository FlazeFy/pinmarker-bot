from fastapi import APIRouter, HTTPException
from services.modules.track.track_queries import get_tracks, get_tracks_period, get_last_tracker_position_api, get_track_by_year_query
from datetime import datetime
from pydantic import BaseModel

router_track = APIRouter()

# GET Query
@router_track.get("/api/v1/track/journey/{id}", response_model=dict)
async def get_current_track(id: str):
    try:
        return await get_tracks(userId=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_track.get("/api/v1/track/last/{id}", response_model=dict)
async def get_last_track(id: str):
    try:
        return await get_last_tracker_position_api(userId=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_track.get("/api/v1/track/year/{year}/{id}", response_model=dict)
async def get_track_by_year(year:int, id: str):
    try:
        return await get_track_by_year_query(userId=id, year=year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class TrackPeriodRequest(BaseModel):
    start_time: datetime
    end_time: datetime
@router_track.get("/api/v1/track/journey/period/{id}", response_model=dict)
async def get_track_journey(id: str, request: TrackPeriodRequest):
    try:
        return await get_tracks_period(userId=id, start_time=request.start_time, end_time=request.end_time)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))