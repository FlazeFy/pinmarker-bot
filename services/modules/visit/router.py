from fastapi import APIRouter, HTTPException, Path, Request
from helpers.docs import generate_dummy
from services.modules.visit.visit_queries import get_all_visit, get_all_visit_last_day
from services.modules.visit.visit_commands import post_visit_query

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
    
@router_visit.post("/api/v1/visit", response_model=dict, 
    summary="Create a visit (MySql)",
    description="This request is used to create a new visit",
    tags=["Visit"],
    responses={
        201: {
            "description": "Successful created visit",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Visit created",
                        "data": {
                            "pin_id": "049f5af1-7a22-4fea-adc3-dae717a45581",
                            "visit_desc": "asd at asdasd",
                            "visit_by": "Personal Car",
                            "visit_with": "Leo",
                            "created_by": "fcazf23e-e5aa-a02m-asd0-3216422910e9",
                            "id": "539c7164-67f3-9c03-2029-d83de1259182",
                            "created_at": "2024-10-21T15:56:38.340159",
                            "pin_name": "My Kost"
                        },
                        "count": 1
                    }
                }
            }
        },
        400: {
            "description": "Failed to insert to db",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Something error! Please call admin",
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User account not found",
                    }
                }
            }
        },
        404: {
            "description": "Pin not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Selected pin is not found",
                    }
                }
            }
        },
        422: {
            "description": "Failed to validate the data",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Validation failed",
                        "errors": [
                            [
                                {
                                    "field": "Visit By",
                                    "message": "Visit By cant be empty"
                                }
                            ]
                        ]
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
async def post_visit_api(request : Request):
    try:
        data = await request.json()
        return await post_visit_query(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))