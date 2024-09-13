from fastapi import APIRouter, HTTPException
from services.modules.user.user_queries import get_check_context_query, get_all_user
from services.modules.user.validate_request_commands import post_req_register_command, post_validate_regis_command
router_user = APIRouter()

# POST Query
@router_user.get("/api/v1/user/check/{type}/{context}", response_model=dict)
async def get_check_context(type: str, context: str):
    try:
        return await get_check_context_query(type=type, context=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_user.get("/api/v2/user", response_model=dict)
async def get_all_user_api():
    try:
        return await get_all_user()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_user.post("/api/v1/req/{type}/{email}/{username}", response_model=dict)
async def post_req_register(type:str, email: str, username: str):
    try:
        return await post_req_register_command(email=email, username=username, type=type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_user.post("/api/v1/req_validate/{type}/{token}/{username}", response_model=dict)
async def post_validate_regis(type:str,token: str, username: str):
    try:
        return await post_validate_regis_command(token=token, username=username, type=type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))