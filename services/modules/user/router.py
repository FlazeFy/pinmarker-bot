from fastapi import APIRouter, HTTPException, Path
from services.modules.user.user_queries import get_check_context_query, get_all_user
from services.modules.user.validate_request_commands import post_req_register_command, post_validate_regis_command
from helpers.docs import generate_dummy
router_user = APIRouter()

# POST Query
@router_user.get("/api/v1/user/check/{type}/{context}", response_model=dict, 
    summary="Get Check User Context (MySql)",
    description="This request is used to check avaiablity of email or username that will be used by checking all account. The `type` are `email` or `username` and `context` is the value",
    tags=["User"],
    responses={
        200: {
            "description": "Email or Username is available to used and have not used in any account",
            "content": {
                "application/json": {
                    "example": {
                        "is_found": False,
                        "message": "Email or Username available",
                    }
                }
            }
        },
        409: {
            "description": "Email or Username is not available to used because have been used in another account",
            "content": {
                "application/json": {
                    "example": {
                        "is_found": True,
                        "message": "Email or Username not available",
                    }
                }
            }
        },
        422: {
            "description": "Email or username failed to pass the validation",
            "content": {
                "application/json": {
                    "example": {
                        "is_found": None,
                        "message": "Email or Username invalid, total character must more than {minChar} and below {maxChar}",
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
async def get_check_context(type: str = Path(..., example='username'), context: str = Path(..., example=generate_dummy(type='username'))):
    try:
        return await get_check_context_query(type=type, context=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_user.get("/api/v2/user", response_model=dict, 
    summary="Get All User (MySql)",
    description="This request is used to get all user registered in this apps",
    tags=["User"],
    responses={
        200: {
            "description": "Successful fetch all registered user",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "00c4a63d-0a0a-5c13-0b4a-58dbd8764729",
                                "username": "12313123",
                                "email": "flazen.edu@gmail.com",
                                "telegram_user_id": "12345678",
                                "telegram_is_valid": 0,
                                "created_at": "2024-09-13T11:23:20",
                                "total_pin": 0,
                                "total_dictionary": 0
                            }
                        ],
                        "message": "User found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Registered user not found",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "User not found",
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
async def get_all_user_api():
    try:
        return await get_all_user()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_user.post("/api/v1/req/{type}/{email}/{username}", response_model=dict, 
    summary="Post Request Register or Forget Password (MySql, Gmail, and Telegram)",
    description="This request is used to ask for token permission of `register` to PinMarker by check the given `email` and `username` first. And at the same time this request can be used for ask for `forget password` token by check the given `email` and `username` that has been registered. The response is also come with `email` and `telegram message` sended to user",
    tags=["User"],
    status_code=201,
    responses={
        201: {
            "description": "Successfuly check avaiability of the request and send the token to user email or telegram account",
            "content": {
                "application/json": {
                    "example": {
                        "is_sended": True,
                        "message": "Token register or Token password recovery is sended to your email!"
                    }
                }
            }
        },
        409: {
            "description": "There's is still an unvalidated request that need to be validated by user",
            "content": {
                "application/json": {
                    "example": {
                        "is_sended": False,
                        "message": "Generate token failed. There's still an unvalidated request",
                    }
                }
            }
        },
        422: {
            "description": "The type request is not valid cause not match to register or forget",
            "content": {
                "application/json": {
                    "example": {
                        "is_sended": None,
                        "message": "Type request not valid",
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
async def post_req_register(type:str = Path(..., example='register'), email: str = Path(..., example=generate_dummy(type='email')), username: str = Path(..., example=generate_dummy(type='username'))):
    try:
        return await post_req_register_command(email=email, username=username, type=type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_user.post("/api/v1/req_validate/{type}/{token}/{username}", response_model=dict, 
    summary="Post Validate Token Register or Forget Password (MySql)",
    description="This request is used to validate the `token` based on given `type` and `username`",
    tags=["User"],
    status_code=201,
    responses={
        201: {
            "description": "Successfuly validate the register or forget password token and giving user access permission",
            "content": {
                "application/json": {
                    "example": {
                        "is_validated": True,
                        "message": "Token is validated!"
                    }
                }
            }
        },
        404: {
            "description": "The token is wrong",
            "content": {
                "application/json": {
                    "example": {
                        "is_validated": False,
                        "message": "Token not found!"
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
async def post_validate_regis(type:str = Path(..., example='register'),token: str = Path(..., example=generate_dummy(type='token')), username: str = Path(..., example=generate_dummy(type='username'))):
    try:
        return await post_validate_regis_command(token=token, username=username, type=type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))