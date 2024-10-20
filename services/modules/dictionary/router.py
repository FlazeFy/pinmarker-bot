from fastapi import APIRouter, HTTPException, Path
from services.modules.dictionary.queries import get_all_dct_by_type_query
from helpers.docs import generate_dummy

router_dct = APIRouter()
    
@router_dct.get("/api/v1/dct/{dct_type}/{user_id}", response_model=dict, 
    summary="Get All Dictionary By Type (MySql)",
    description="This request is used to get all dictionary by 'dct_type' and based from 'user_id' for specific category",
    tags=["Dictionary"],
    responses={
        200: {
            "description": "Successful fetch all dictionary",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "dictionary_name": "apaini",
                                "dictionary_color": "orange"
                            }
                        ],
                        "message": "Dictionary found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Dictionary not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Dictionary not found",
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
async def get_all_dct_by_type_api(dct_type: str= Path(..., example=generate_dummy(type='dct_type'), max_length=36),user_id: str= Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_all_dct_by_type_query(dct_type=dct_type, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))