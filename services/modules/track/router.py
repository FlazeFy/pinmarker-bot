from fastapi import APIRouter, HTTPException
from services.modules.track.track_queries import get_tracks, get_tracks_period, get_last_tracker_position_api, get_total_distance_by_month_query, get_total_distance_by_time_query, get_activity_around_coordinate_query
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
async def get_total_distance_by_month(year:int, id: str):
    try:
        return await get_total_distance_by_month_query(userId=id, year=year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_track.get("/api/v1/track/hour/{year}/{id}", response_model=dict)
async def get_total_distance_by_time(year:int, id: str):
    try:
        return await get_total_distance_by_time_query(userId=id, year=year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_track.get("/api/v1/track/journey_day/{date}/{id}", response_model=dict)
async def get_track_journey_by_date(date: str, id: str):
    try:
        start_time = datetime.strptime(date + "T00:00:01", "%Y-%m-%dT%H:%M:%S")
        end_time = datetime.strptime(date + "T23:59:59", "%Y-%m-%dT%H:%M:%S")
        return await get_tracks_period(userId=id, start_time=start_time, end_time=end_time)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_track.get("/api/v1/track/activity_around/{coor}/{id}", response_model=dict)
async def get_activity_around_coordinate(coor: str, id: str):
    try:
        return await get_activity_around_coordinate_query(userId=id, coor=coor)
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