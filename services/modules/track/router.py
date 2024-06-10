from fastapi import APIRouter, HTTPException
from services.modules.track.track_queries import get_tracks, get_tracks_period
from datetime import datetime
from pydantic import BaseModel

router_track = APIRouter()

# GET Query
@router_track.get("/api/v1/track/journey/{id}", response_model=dict)
async def get_all_my_project_v1(id: str):
    try:
        return await get_tracks(userId=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class TrackPeriodRequest(BaseModel):
    start_time: datetime
    end_time: datetime
@router_track.get("/api/v1/track/journey/period/{id}", response_model=dict)
async def get_all_my_project_v1(id: str, request: TrackPeriodRequest):
    try:
        return await get_tracks_period(userId=id, start_time=request.start_time, end_time=request.end_time)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))