from fastapi import APIRouter, HTTPException, Request
from services.modules.bot_relation.command import post_check_bot_relation

router_bot_relation = APIRouter()
    
@router_bot_relation.post("/api/v1/bot_relation/check", response_model=dict, 
    summary="Post Check Bot Relation (MySql)",
    description="This request is used to check if sender chat to Bot is registered or not",
    tags=["Bot Relation"],
    status_code=200,
    responses={
        200: {
            "description": "Successful check the bot relation",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Relation checked",
                        "data": {
                            "context_id": "123456789",
                            "relation_type": "group",
                            "relation_platform":"line",
                            "relation_name":"Group Testing",
                            "expired_at":"2024-08-26T21:31:00",
                            "created_at":"2024-08-26T21:31:00"
                        },
                    }
                }
            }
        },
        404: {
            "description": "Something wrong with the query",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Relation not found",
                    }
                }
            }
        },
        422: {
            "description": "request body dont pass the validation",
            "content": {
                "application/json": {
                    "example": {
                        "message": "relation type not valid",
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
async def post_check_bot_relation_api(request : Request):
    try:
        data = await request.json()
        return await post_check_bot_relation(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))