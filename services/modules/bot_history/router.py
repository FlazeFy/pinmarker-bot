from fastapi import APIRouter, HTTPException, Path
from services.modules.bot_history.queries import get_bot_history
from helpers.docs import generate_dummy

router_bot_history = APIRouter()

# GET Query
@router_bot_history.get("/api/v1/bot_history/{socmed_id}", response_model=dict, 
    summary="Get Bot History (SQFlite)",
    description="This request is used to retrieve the history of menu or command interactions from telegram or discord bot using the given `socmed_id`",
    tags=["Bot History"],
    responses={
        200: {
            "description": "Successful retrieval of bot history.",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "command": "/Stats",
                                "created_at": "2024-09-11 14:32:09",
                                "total": 1
                            }
                        ],
                        "message": "History found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Bot history not found for the given `socmed_id`",
            "content": {
                "application/json": {
                    "example": {
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
async def get_bot_history_api(socmed_id: str = Path(..., example=generate_dummy(type='socmed_id'))):
    try:
        return await get_bot_history(socmed_id=socmed_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))