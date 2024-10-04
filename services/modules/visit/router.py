from fastapi import APIRouter, HTTPException, Path
from helpers.docs import generate_dummy
from services.modules.visit.visit_queries import get_all_visit

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