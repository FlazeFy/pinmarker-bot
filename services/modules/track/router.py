from fastapi import APIRouter, HTTPException, Path
from services.modules.track.track_queries import get_tracks, get_tracks_period, get_last_tracker_position_api, get_total_distance_by_month_query, get_total_distance_by_time_query, get_activity_around_coordinate_query
from datetime import datetime
from pydantic import BaseModel
from helpers.docs import generate_dummy

router_track = APIRouter()

dummy_coordinate = f"{generate_dummy(type='lat')},{generate_dummy(type='long')}"

# GET Query
@router_track.get("/api/v1/track/journey/{user_id}", response_model=dict, 
    summary="Get Track (Firebase Realtime)",
    description="This request is used to get recent track history based on given `user_id`",
    tags=["Track"],
    responses={
        200: {
            "description": "Successful fetch recent track history for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "battery_indicator": 48,
                                "created_at": "2024-09-13T23:46:00.561424",
                                "created_by": "fcd3f23e-e5aa-11ee-892a-3216422910e9",
                                "track_lat": -6.226764,
                                "track_long": 106.8220981,
                                "track_type": "live"
                            }
                        ],
                        "message": "Track journey found",
                        "count": 10
                    }
                }
            }
        },
        404: {
            "description": "Track history not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "No Track journey found",
                        "count": 0
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "[Error message]"
                    }
                }
            }
        }
    })
async def get_current_track(user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_tracks(userId=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_track.get("/api/v1/track/last/{user_id}", response_model=dict, 
    summary="Get Last Track (Firebase Realtime)",
    description="This request is used to get last track based on given `user_id`",
    tags=["Track"],
    responses={
        200: {
            "description": "Successful fetch last track for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data":
                        {
                            "battery_indicator": 48,
                            "created_at": "2024-09-13T23:46:00.561424",
                            "created_by": "fcd3f23e-e5aa-11ee-892a-3216422910e9",
                            "track_lat": -6.226764,
                            "track_long": 106.8220981,
                            "track_type": "live"
                        },
                        "message": "Last track found",
                    }
                }
            }
        },
        404: {
            "description": "Track not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "No Track found",
                        "count": 0
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "[Error message]"
                    }
                }
            }
        }
    })
async def get_last_track(user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_last_tracker_position_api(userId=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_track.get("/api/v1/track/year/{year}/{user_id}", response_model=dict, 
    summary="Get Total Distance Per Month (Firebase Realtime)",
    description="This request is used to get total distance traveled (meters) per month in a year. based on given `user_id` and `year`",
    tags=["Track"],
    responses={
        200: {
            "description": "Successful fetch total distance traveled for given user id and year",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "context": 5,
                                "total": 0.4835698343530167
                            },
                        ],
                        "data_detail": [
                            {
                                "created_at": "2024-05-10T10:27:55.625272",
                                "month": 5
                            },
                        ],
                        "message": "Track journey found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Total distance traveled not found for given user id and year",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "data_detail": None,
                        "message": "No Track journey found",
                        "count": 0
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "[Error message]"
                    }
                }
            }
        }
    })
async def get_total_distance_by_month(year:int = Path(..., example=generate_dummy(type='year')), user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_total_distance_by_month_query(userId=user_id, year=year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_track.get("/api/v1/track/hour/{year}/{user_id}", response_model=dict, 
    summary="Get Total Distance Per Hour (Firebase Realtime)",
    description="This request is used to get total distance traveled (meters) per hour in a year. based on given `user_id` and `year`",
    tags=["Track"],
    responses={
        200: {
            "description": "Successful fetch total distance traveled for given user id and year",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "context": 18,
                                "total": 0.4835698343530167
                            },
                        ],
                        "data_detail": [
                            {
                                "created_at": "2024-05-10T10:27:55.625272",
                                "month": 5
                            },
                        ],
                        "message": "Track journey found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Total distance traveled not found for given user id and year",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "data_detail": None,
                        "message": "No Track journey found",
                        "count": 0
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "[Error message]"
                    }
                }
            }
        }
    })
async def get_total_distance_by_time(year:int = Path(..., example=generate_dummy(type='year')), user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_total_distance_by_time_query(userId=user_id, year=year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_track.get("/api/v1/track/journey_day/{date}/{user_id}", response_model=dict, 
    summary="Get Track by date (Firebase Realtime)",
    description="This request is used to get track history in a day based on given `user_id` and `date`",
    tags=["Track"],
    responses={
        200: {
            "description": "Successful fetch track history by day for given user id and date",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "battery_indicator": 48,
                                "created_at": "2024-09-13T23:46:00.561424",
                                "created_by": "fcd3f23e-e5aa-11ee-892a-3216422910e9",
                                "track_lat": -6.226764,
                                "track_long": 106.8220981,
                                "track_type": "live"
                            }
                        ],
                        "message": "Track journey found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Track history by day not found for given user id and date",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "No Track journey found",
                        "count": 0
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "[Error message]"
                    }
                }
            }
        }
    })
async def get_track_journey_by_date(date: str = Path(..., example=generate_dummy(type='date'), max_length=10, min_length=10), user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        start_time = datetime.strptime(date + "T00:00:01", "%Y-%m-%dT%H:%M:%S")
        end_time = datetime.strptime(date + "T23:59:59", "%Y-%m-%dT%H:%M:%S")
        return await get_tracks_period(userId=user_id, start_time=start_time, end_time=end_time)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_track.get("/api/v1/track/activity_around/{coordinate}/{user_id}", response_model=dict, 
    summary="Get Track Activity Around Coordinate (Firebase Realtime)",
    description="This request is used to get track history near a given `coordinate` and by its `user_id`",
    tags=["Track"],
    responses={
        200: {
            "description": "Successful fetch track history near a given coordinate and by its user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "created_at": "2024-05-10T10:27:55.625272",
                                "date": "2024-05-10T10:27:55.625272",
                                "distance": 8212.104097826523
                            }
                        ],
                        "message": "Track activity found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "track history near a given coordinate and by its user id not found",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "No Track activity found",
                        "count": 0
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "[Error message]"
                    }
                }
            }
        }
    })
async def get_activity_around_coordinate(coordinate: str = Path(..., example=dummy_coordinate, max_length=72, min_length=10), user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_activity_around_coordinate_query(userId=user_id, coor=coordinate)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class TrackPeriodRequest(BaseModel):
    start_time: datetime
    end_time: datetime
@router_track.post("/api/v1/track/journey/period/{user_id}", response_model=dict, 
    summary="Get Track Activity Around Specific Date (Firebase Realtime)",
    description="This request is used to get track history in a period of time based on given `start_time`, `end_time`, and by its `user_id`",
    tags=["Track"],
    status_code=200,
    responses={
        200: {
            "description": "Successful fetch track history in a period of time based on given start time, end time, and by its user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "battery_indicator": 92,
                                "created_at": "2024-06-10T10:27:59.914790",
                                "created_by": "fcd3f23e-e5aa-11ee-892a-3216422910e9",
                                "track_lat": -6.226732,
                                "track_long": 106.8220708,
                                "track_type": "live"
                            }
                        ],
                        "message": "Track journey found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Track history in a period of time based on given start time, end time, and by its user id not found",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "No Track journey found",
                        "count": 0
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "[Error message]"
                    }
                }
            }
        }
    })
async def get_track_journey(request: TrackPeriodRequest, user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        print(request)
        return await get_tracks_period(userId=user_id, start_time=request.start_time, end_time=request.end_time)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))