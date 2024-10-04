from fastapi import APIRouter, HTTPException, Request, Path
from helpers.docs import generate_dummy
from services.modules.history.queries import get_all_history

router_history = APIRouter()

# GET Query
@router_history.get("/api/v1/history/{user_id}", response_model=dict, 
    summary="Get All History (MySql)",
    description="This request is used to get all history `user_id`",
    tags=["History"],
    responses={
        200: {
            "description": "Successful fetch all history by user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "fcd3f23e-e5aa-11ee-892a-3216422910e9",
                                "history_type": "Add Marker",
                                "history_context": "My Kost",
                                "created_at": "2024-03-18T06:47:27"
                            }
                        ],
                        "message": "History found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "History not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "History not found",
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
async def get_all_history_api(user_id: str= Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_all_history(userId=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))