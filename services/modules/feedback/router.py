from fastapi import APIRouter, HTTPException, Request
from services.modules.feedback.command import post_feedback
from services.modules.feedback.queries import get_feedback

router_feedback = APIRouter()

# POST Command
@router_feedback.post("/api/v1/feedback", response_model=dict, 
    summary="Send Feedback (MySql)",
    description="This request is used to send feedback about the apps anonymously",
    tags=["Feedback"],
    responses={
        201: {
            "description": "Successful send the feedback",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Feedback inserted",
                        "data": {
                            "feedback_body": "test",
                            "feedback_rate": 3
                        },
                        "count": 1
                    }
                }
            }
        },
        400: {
            "description": "Something wrong with the query",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Feedback failed to insert",
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
async def post_feedback_api(request : Request):
    try:
        data = await request.json()
        return await post_feedback(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_feedback.get("/api/v1/feedback", response_model=dict, 
    summary="Get All Feedback (MySql)",
    description="This request is used to get all feedback from user",
    tags=["Feedback"],
    responses={
        200: {
            "description": "Successful fetch all feedback",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "feedback_rate": 3,
                                "feedback_body": "test",
                                "created_at": "2024-09-14T06:41:23"
                            }
                        ],
                        "message": "Feedback found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Feedback not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Feedback not found",
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
async def get_feedback_api():
    try:
        return await get_feedback()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))