from fastapi import APIRouter, HTTPException, Path
from helpers.docs import generate_dummy
from services.modules.visit.visit_queries import get_all_visit, get_all_visit_last_day

router_visit = APIRouter()

# GET Query
@router_visit.get("/api/v1/visit/{user_id}", response_model=dict, 
    summary="Get All Visit (MySql)",
    description="This request is used to get all visit `user_id`",
    tags=["Visit"],
    responses={
        200: {
            "description": "Successful fetch all visit by user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "cdafe52c-d36e-96b9-17ee-56c0ef7964d3",
                                "visit_desc": "Test visit",
                                "visit_by": "Personal Car",
                                "visit_with": "Leonardho R Sitanggang",
                                "created_at": "2024-08-26T14:31:00",
                                "pin_name": "Alya Kost"
                            }
                        ],
                        "message": "Visit found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Visit not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Visit not found",
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
async def get_all_visit_api(user_id: str= Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_all_visit(userId=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_visit.get("/api/v1/visit/history/{user_id}/{days}", response_model=dict, 
    summary="Get All Visit History in Last -n Days (MySql)",
    description="This request is used to get all history visit in `days` by given `user_id`",
    tags=["Visit"],
    responses={
        200: {
            "description": "Successful fetch all visit history by user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "pin_name": "My Kost",
                                "visit_desc": "Lorem ipsum",
                                "visit_by": "Personal Car",
                                "visit_with": "Leonardho R Sitanggang",
                                "created_at": "2024-08-26T21:31:00"
                            }
                        ],
                        "message": "Visit history found",
                        "count": 1,
                        "with_timezone": True
                    }
                }
            }
        },
        404: {
            "description": "Visit history not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Visit history not found",
                        "count": 0,
                        "with_timezone": None
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
async def get_all_visit_history_api(user_id: str= Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36),days: str= Path(..., example="30")):
    try:
        return await get_all_visit_last_day(userId=user_id, days=days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))