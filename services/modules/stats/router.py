from fastapi import APIRouter, HTTPException, Path
from services.modules.stats.stats_queries import get_dashboard
from services.modules.stats.template import get_total_item_by_context
from fastapi.responses import JSONResponse
from helpers.docs import generate_dummy
from enum import Enum

router_stats = APIRouter()

class TypeEnumRole(str, Enum):
    admin = "admin"
    user = "user"

# GET Query
@router_stats.get("/api/v1/stats/dashboard/{user_id}/{role}", response_model=dict, 
    summary="Get stats dashboard (MySql)",
    description="This request is used to get stats dashboard like format based on given `user_id` and `role`",
    tags=["Stats"],
    responses={
        200: {
            "description": "Successful fetch dashboard stats by user id and role",
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "total_marker": 20,
                            "total_favorite": 2,
                            "most_category": "(12) friend",
                            "last_added": "Cafe A",
                            "last_visit": "My Kost",
                            "most_visit": "(10) My Kost"
                        },
                        "message": "Dashboard found"
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
async def get_dashboard_route(user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36), role:TypeEnumRole = Path(..., example="user")):
    try:
        return await get_dashboard(userId=user_id, role=role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router_stats.get("/api/v1/stats/total_pin_by_category/{user_id}", response_model=dict, 
    summary="Get Total Pin By Category (MySql)",
    description="This request is used to get stats total pin for each category like based on given `user_id`. This returned response have reusable format for used in chart template",
    tags=["Stats"],
    responses={
        200: {
            "description": "Successful fetch total pin for each category for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "context": "Friend",
                                "total": 6
                            }
                        ],
                        "message": "Stats found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Total pin not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "No Stats found",
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
async def get_total_pin_by_category(user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        data = await get_total_item_by_context(tableName="pin", join=None, targetColumn="pin_category", userId=user_id, where=None)
        if len(data) != 0:
            data_list = [dict(row._mapping) for row in data]
            return JSONResponse(
                status_code=200, 
                content={
                    "data": data_list,
                    "message": "Stats found",
                    "count": len(data)
                }
            )
        else:
            return JSONResponse(
                status_code=404, 
                content={
                    "data": None,
                    "message": "No Stats found",
                    "count": 0
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_stats.get("/api/v1/stats/total_visit_by_category/{user_id}", response_model=dict, 
    summary="Get Total Visit By Category (MySql)",
    description="This request is used to get stats total visit for each category like based on given `user_id`. This returned response have reusable format for used in chart template",
    tags=["Stats"],
    responses={
        200: {
            "description": "Successful fetch total visit for each category for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "context": "Personal Car",
                                "total": 6
                            }
                        ],
                        "message": "Stats found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Total visit not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "No Stats found",
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
async def get_total_visit_by_category(user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        data = await get_total_item_by_context(tableName="visit", join="pin on pin.id = visit.pin_id", targetColumn="pin_category", userId=user_id, where=None)
        if len(data) != 0:
            data_list = [dict(row._mapping) for row in data]
            return JSONResponse(
                status_code=200, 
                content={
                    "data": data_list,
                    "message": "Stats found",
                    "count": len(data)
                }
            )
        else:
            return JSONResponse(
                status_code=404, 
                content={
                    "data": None,
                    "message": "No Stats found",
                    "count": 0
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_stats.get("/api/v1/stats/total_visit_by_category/{user_id}/{pin_id}", response_model=dict, 
    summary="Get Total Visit By Category and Pin (MySql)",
    description="This request is used to get stats total visit for each category from a pin based on given `user_id` and `pin_id`. This returned response have reusable format for used in chart template",
    tags=["Stats"],
    responses={
        200: {
            "description": "Successful fetch total visit for each category for given user id and pin id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "context": "Personal Car",
                                "total": 6
                            }
                        ],
                        "message": "Stats found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Total visit not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "No Stats found",
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
async def get_total_visit_by_category_by_pin(user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36),pin_id: str = Path(..., example=generate_dummy(type='pin_id'), max_length=36, min_length=36)):
    try:
        data = await get_total_item_by_context(tableName="visit", join="pin on pin.id = visit.pin_id", targetColumn="pin_category", userId=user_id, where=f"pin.id = '{pin_id}'")
        if len(data) != 0:
            data_list = [dict(row._mapping) for row in data]
            return JSONResponse(
                status_code=200, 
                content={
                    "data": data_list,
                    "message": "Stats found",
                    "count": len(data)
                }
            )
        else:
            return JSONResponse(
                status_code=404, 
                content={
                    "data": None,
                    "message": "No Stats found",
                    "count": 0
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_stats.get("/api/v1/stats/total_gallery_by_pin/{user_id}", response_model=dict, 
    summary="Get Total Gallery By Pin (MySql)",
    description="This request is used to get stats total gallery for each pin like based on given `user_id`. This returned response have reusable format for used in chart template",
    tags=["Stats"],
    responses={
        200: {
            "description": "Successful fetch total gallery for each pin for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "context": "Cafe A",
                                "total": 6
                            }
                        ],
                        "message": "Stats found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Total gallery not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "No Stats found",
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
async def get_total_gallery_by_pin(user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        data = await get_total_item_by_context(tableName="gallery", join="pin on pin.id = gallery.pin_id", targetColumn="pin_name", userId=user_id,where=None)
        if len(data) != 0:
            data_list = [dict(row._mapping) for row in data]
            return JSONResponse(
                status_code=200, 
                content={
                    "data": data_list,
                    "message": "Stats found",
                    "count": len(data)
                }
            )
        else:
            return JSONResponse(
                status_code=404, 
                content={
                    "data": None,
                    "message": "No Stats found",
                    "count": 0
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    