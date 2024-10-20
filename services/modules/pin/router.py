from fastapi import APIRouter, HTTPException, Request, Path
from services.modules.pin.pin_queries import get_all_pin, get_pin_by_category_query,get_all_pin_export_query,get_global_list_query,get_nearest_pin_query,get_detail_list_by_id_query,get_global_pin_by_list_id,get_pin_detail_history_by_id_or_name,get_pin_distance_to_my_personal_pin_by_id,get_trash_pin,get_nearest_global_pin_query
from services.modules.pin.pin_commands import soft_delete_pin_by_id,recover_pin_by_id,hard_delete_pin_by_id,put_pin_favorite,post_pin_query
from helpers.docs import generate_dummy

router_pin = APIRouter()

# For Telegram, Web, and Mobile
# GET Query
@router_pin.get("/api/v1/pin/{user_id}", response_model=dict, 
    summary="Get All Pin - for User (MySql)",
    description="This request is used to get pin based on given `user_id`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch all pin by user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "049f5af1-7a22-4fea-adc3-dae717a45581",
                                "pin_name": "Warteg D Amertha",
                                "pin_desc": "Warteg murmer langganan depan gapura D Amertha. Parkir di depan gapura. Minggu tutup",
                                "pin_coordinate": "-6.977430240726936,107.65112376402404",
                                "pin_category": "Restaurant",
                                "pin_person": "Bude",
                                "is_favorite": False,
                                "pin_address": "D Amertha Residence",
                                "created_at": "2024-03-18T06:47:27",
                                "total_visit": 6,
                                "last_visit": "2024-08-19T11:00:00"
                            }
                        ],
                        "message": "Pin found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
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
async def get_all_pin_api(user_id: str= Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_all_pin(userId=user_id, platform='telegram')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin_export/{user_id}", response_model=dict, 
    summary="Get All Pin - Export Format (MySql)",
    description="This request is used to get pin based on given `user_id` and `` but the result is designed for import format (CSV) in PinMarker Web",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch all pin by user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "pin_name": "123123",
                                "pin_lat": "-6.2028299038609305",
                                "pin_long": "106.90157343394769"
                            }
                        ],
                        "message": "Pin found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
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
async def get_all_pin_export_api(user_id: str= Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_all_pin_export_query(userId=user_id, platform='telegram')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin/{pin_category}/{user_id}", response_model=dict, 
    summary="Get Pin By Category (MySql)",
    description="This request is used to get pin based on given `user_id` and `category`. The category is separated by comma",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch all pin by user id and categories",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "pin_name": "Warteg D Amertha",
                                "pin_desc": "Warteg murmer langganan depan gapura D Amertha. Parkir di depan gapura. Minggu tutup",
                                "pin_lat": "-2.5959778412319934",
                                "pin_long": "140.6414633989334",
                                "pin_person": "Bude",
                                "pin_address": "D Amertha Residence",
                                "pin_call": "123123",
                                "pin_email": "warteg@gmail.com",
                            }
                        ],
                        "message": "Pin found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found for given user id and categories",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
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
# category can be multiple and separate by comma
# ex : cafe,restaurant
async def get_pin_by_category(pin_category: str = Path(..., example=generate_dummy(type='pin_category')), user_id: str = Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36)):
    try:
        return await get_pin_by_category_query(category=pin_category, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin_global/{search}", response_model=dict, 
    summary="Get Global Pin (MySql)",
    description="This request is used to get list of pin based on given `search` key. The search key can be `list_name`, `pin_name`, `list_tag`, and the owner (`username`)",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch all global pin by search key",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "e396661c-5797-11ef-a5a5-3216422910e8",
                                "pin_list": "pinpin,Roti Romi,PLANET CELL,PARMAN CELL,reivan cell,My Kost,234 CELL 2,Warteg D Amertha,SULTAN CELL 1,GOES CELL",
                                "total": 10,
                                "list_name": "Dessert Trips",
                                "list_desc": "push glukosa",
                                "list_tag": [
                                    {
                                        "tag_name": "Weekend"
                                    },
                                    {
                                        "tag_name": "Dessert"
                                    },
                                    {
                                        "tag_name": "Jakarta"
                                    }
                                ],
                                "created_at": "2024-08-11T06:11:30",
                                "created_by": "flazefy"
                            }
                        ],
                        "message": "Pin found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Global Pin not found for given search key",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
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
async def get_global_list_api(search: str = Path(..., example=generate_dummy(type='search'))):
    try:
        return await get_global_list_query(search=search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.post("/api/v1/pin/nearest/{lat}/{long}", response_model=dict, 
    summary="Get Nearest Pin (MySql)",
    description="This request is used to get nearest pin based on given `lat`, `long`, `user_id`, `max_distance` from the coordinate, and `limit`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch all pin by lat, long, user id, max distance from the coordinate, and limit",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "pin_name": "My Office - AGIT x TSEL",
                                "pin_desc": "Lorem ipsum",
                                "pin_coor": "-6.2302963368641056,106.81831151247025",
                                "pin_category": "Office",
                                "pin_address": "Jl. Gatot Soebroto",
                                "pin_person": "Leonardho R Sitanggang",
                                "pin_call": "08114882001",
                                "pin_email": "flazen.edu@gmail.com",
                                "distance": 682.0905337122441
                            }
                        ],
                        "message": "Pin found",
                        "is_found_near": True,
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found for given lat, long, user id, max distance from the coordinate, and limit",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
                        "is_found_near": False,
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
async def get_nearest_pin_api(
        request : Request,
        lat: str = Path(..., example=generate_dummy(type='lat'), max_length=36, min_length=4), 
        long:str = Path(..., example=generate_dummy(type='long'), max_length=37, min_length=5), 
    ):
    try:
        data = await request.json()
        return await get_nearest_pin_query(lat=lat, long=long, userid=data.get('user_id'), max_dis=data.get('max_distance'), limit=data.get('limit'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.post("/api/v1/pin_global/nearest/{lat}/{long}", response_model=dict, 
    summary="Get Nearest Global Pin (MySql)",
    description="This request is used to get nearest pin based on given `lat`, `long`, `max_distance` from the coordinate, and `limit`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch all global pin by lat, long, max distance from the coordinate, and limit",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "pin_name": "My Office - AGIT x TSEL",
                                "pin_desc": "Lorem ipsum",
                                "pin_coor": "-6.2302963368641056,106.81831151247025",
                                "pin_category": "Office",
                                "pin_address": "Jl. Gatot Soebroto",
                                "pin_person": "Leonardho R Sitanggang",
                                "pin_call": "08114882001",
                                "pin_email": "flazen.edu@gmail.com",
                                "distance": 682.0905337122441
                            }
                        ],
                        "message": "Global Pin found",
                        "is_found_near": True,
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found for given lat, long, max distance from the coordinate, and limit",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Global Pin not found",
                        "is_found_near": False,
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
async def get_nearest_global_pin_api(
        request : Request,
        lat: str = Path(..., example=generate_dummy(type='lat'), max_length=36, min_length=4), 
        long:str = Path(..., example=generate_dummy(type='long'), max_length=37, min_length=5), 
    ):
    try:
        data = await request.json()
        return await get_nearest_global_pin_query(lat=lat, long=long, max_dis=data.get('max_distance'), limit=data.get('limit'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# For Discord
@router_pin.get("/api/v2/pin", response_model=dict, 
    summary="Get All Pin - for Admin (MySql)",
    description="This request is used to get all pin",
    tags=["Pin (v2 - Admin)"],
    responses={
        200: {
            "description": "Successful fetch all pin",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "pin_name": "Cafe B",
                                "pin_desc": "Lorem Ipsum",
                                "pin_coordinate": "- hidden -",
                                "pin_category": "Cafe",
                                "pin_person": "123123",
                                "pin_address": "- hidden -",
                                "pin_call": "08123456789",
                                "pin_email": "flazen.edu@gmail.com",
                                "created_at": "2024-07-15T00:12:59",
                                "created_by": "flazefy",
                                "is_global_shared": False
                            }
                        ],
                        "message": "Pin found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
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
async def get_all_pin_api():
    try:
        return await get_all_pin(userId=None, platform='discord')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v2/pin_export", response_model=dict, 
    summary="Get All Pin - for Admin Export Format (MySql)",
    description="This request is used to get all pin but the result is designed for import format (CSV) in PinMarker Web",
    tags=["Pin (v2 - Admin)"],
    responses={
        200: {
            "description": "Successful fetch all pin by user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "pin_name": "Cafe A",
                                "pin_lat": "-6.2028299038609305",
                                "pin_long": "106.90157343394769",
                                "created_at": "2024-07-15T00:12:59",
                                "created_by": "flazefy"
                            }
                        ],
                        "message": "Pin found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
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
async def get_all_pin_export_api():
    try:
        return await get_all_pin_export_query(userId=None, platform='discord')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin_global/{id}/{user_id}", response_model=dict, 
    summary="Get Global List Detail By Id - for User (MySql)",
    description="This request is used to get detail and relation of global list based on given `user_id` and global list's `id`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch detail of global list with all of pin relation by user id and global list id",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "list_name": "Dessert Trips",
                            "list_desc": "push glukosa",
                            "list_tag": [
                            {
                                "tag_name": "Weekend"
                            },
                            {
                                "tag_name": "Dessert"
                            },
                            {
                                "tag_name": "Jakarta"
                            }
                            ],
                            "created_at": "2024-08-11T06:11:30",
                            "updated_at": "2024-08-17T01:19:44",
                            "created_by": "12313123"
                        },
                        "data": [
                            {
                                "id": "c64da478-a237-9a81-2b11-a2baebfed0a8",
                                "pin_name": "Warteg D Amertha",
                                "pin_desc": "Warteg murmer langganan depan gapura D Amertha. Parkir di depan gapura. Minggu tutup",
                                "pin_lat": "-6.977430240726936",
                                "pin_long": "107.65112376402404",
                                "pin_call": "08123456",
                                "pin_category": "Restaurant",
                                "created_at": "2024-09-01T20:23:21",
                                "pin_address": "Jl. Ketupat",
                                "created_by": "flazefy",
                                "gallery_url": "https://leonardhors.com",
                                "gallery_caption": "Ini gambar",
                                "gallery_type": "image"
                            }
                        ],
                        "message": "List and pin found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Global list not found for given user id",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Global list not found",
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
async def get_detail_list_by_id(user_id: str= Path(..., example=generate_dummy(type='user_id'), max_length=36, min_length=36), id:str = Path(..., example=generate_dummy(type='list_id'), max_length=36, min_length=36)):
    try:
        return await get_detail_list_by_id_query(userId=user_id, id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.post("/api/v1/pin_global/search/by_list_id", response_model=dict, 
    summary="Get Global Pin By Some of List ID (MySql)",
    description="This request is used to get global pin based on given set of `list_ids`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch all pin by list ids",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "list_id": "e396661c-5797-11ef-a5a5-3216422910e8",
                                "list_name": "Dessert Trips",
                                "pin_name": "pinpin",
                                "pin_desc": "ini deskripsi",
                                "pin_category": "Outlet Telkomsel",
                                "pin_coordinate": "-6.267563333,106.7964583",
                                "created_at": "2024-08-11T06:11:30",
                                "created_by": "flazefy"
                            }
                        ],
                        "message": "Pin found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found for given list ids",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
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
async def get_global_pin_by_list_id_api(request : Request):
    try:
        data = await request.json()
        return await get_global_pin_by_list_id(list_ids=data.get('list_ids'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin/detail/{id}/{user_id}", response_model=dict, 
    summary="Get Pin Detail and Visit History by Id (MySql)",
    description="This request is used to get pin detail and visit history based on given pin `id` and `user_id`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch pin detail and history",
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "pin_name": "My Kost",
                            "pin_desc": "Kamar A66",
                            "pin_category": "Personal",
                            "pin_lat": "-6.226838579766097",
                            "pin_long": "106.82157923228753",
                            "pin_person": "Leonardho R Sitanggang",
                            "pin_email": "flazen.edu@gmail.com",
                            "pin_call": "08114882001",
                            "pin_address": "",
                            "created_at": "2024-03-16T01:47:22",
                            "updated_at": "2024-08-20T02:52:34"
                        },
                        "message": "Pin found",
                        "history": [
                                {
                                    "visit_desc": "asdads",
                                    "visit_by": "Public Transportation",
                                    "visit_with": "mm",
                                    "created_at": "2024-07-15T11:20:00"
                                },
                            ]
                        }
                }
            }
        },
        404: {
            "description": "Pin not found",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
                        "history": None
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
async def get_pin_detail_history_by_id_api(id: str = Path(..., example=generate_dummy(type='pin_id')),user_id: str = Path(..., example=generate_dummy(type='user_id'))):
    try:
        return await get_pin_detail_history_by_id_or_name(pin_context=id, user_id=user_id,search_by='id')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin/detail/name/{pin_name}/{user_id}", response_model=dict, 
    summary="Get Pin Detail and Visit History by Pin Name (MySql)",
    description="This request is used to get pin detail and visit history based on given pin `pin_name` and `user_id`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch pin detail and history",
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "pin_name": "My Kost",
                            "pin_desc": "Kamar A66",
                            "pin_category": "Personal",
                            "pin_lat": "-6.226838579766097",
                            "pin_long": "106.82157923228753",
                            "pin_person": "Leonardho R Sitanggang",
                            "pin_email": "flazen.edu@gmail.com",
                            "pin_call": "08114882001",
                            "pin_address": "",
                            "created_at": "2024-03-16T01:47:22",
                            "updated_at": "2024-08-20T02:52:34"
                        },
                        "message": "Pin found",
                        "history": [
                                {
                                    "visit_desc": "asdads",
                                    "visit_by": "Public Transportation",
                                    "visit_with": "mm",
                                    "created_at": "2024-07-15T11:20:00"
                                },
                            ]
                        }
                }
            }
        },
        404: {
            "description": "Pin not found",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
                        "history": None
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
async def get_pin_detail_history_by_pin_name_api(pin_name: str = Path(..., example=generate_dummy(type='pin_name')),user_id: str = Path(..., example=generate_dummy(type='user_id'))):
    try:
        return await get_pin_detail_history_by_id_or_name(pin_context=pin_name, user_id=user_id, search_by='name')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin/distance/personal/{id}/{user_id}", response_model=dict, 
    summary="Get Pin Distance to My Personal Pin (MySql)",
    description="This request is used to get pin distance to my personal category pin based on its `id` and `user_id`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch pin distance",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "fcd3f23e-e5aa-11ee-892a-3216422910e9",
                                "pin_name": "My Kost",
                                "pin_desc": "Kamar A66",
                                "pin_lat": "-6.226838579766097",
                                "pin_long": "106.82157923228753",
                                "distance_to_meters": 9.46,
                                "created_at": "2024-03-16T01:47:22",
                            },
                        ],
                        "message": "Pin found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found or the pin derpature is not exist",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found | Pin derpature not found",
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
async def get_pin_distance_to_my_personal_pin_by_id_api(id: str = Path(..., example=generate_dummy(type='pin_id')),user_id: str = Path(..., example=generate_dummy(type='user_id'))):
    try:
        return await get_pin_distance_to_my_personal_pin_by_id(pin_id=id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.delete("/api/v1/pin/soft_del/{id}/{user_id}", response_model=dict, 
    summary="Delete Pin by Id (MySql)",
    description="This request is used to delete (soft-delete) a pin and still can be recovered based on its `id` and `user_id`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful delete pin",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Pin deleted | Pin deleted but failed to write history",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Pin not found",
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
async def soft_delete_pin_by_id_api(id: str = Path(..., example=generate_dummy(type='pin_id')),user_id: str = Path(..., example=generate_dummy(type='user_id'))):
    try:
        return await soft_delete_pin_by_id(pin_id=id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.put("/api/v1/pin/recover/{id}/{user_id}", response_model=dict, 
    summary="Recover deleted Pin by Id (MySql)",
    description="This request is used to recover deleted (soft-delete) pin based on its `id` and `user_id`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful recover deleted pin",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Pin recovered | Pin recovered but failed to write history",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Pin not found",
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
async def recover_pin_by_id_api(id: str = Path(..., example=generate_dummy(type='pin_id')),user_id: str = Path(..., example=generate_dummy(type='user_id'))):
    try:
        return await recover_pin_by_id(pin_id=id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.delete("/api/v1/pin/hard_del/{id}/{user_id}", response_model=dict, 
    summary="Permentally Delete Pin by Id (MySql)",
    description="This request is used to permentally delete (hard-delete) a pin and cant be recovered `id` and `user_id`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful permentally delete pin",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Pin permentally deleted | Pin permentally deleted but failed to write history",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Pin not found",
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
async def hard_delete_pin_by_id_api(id: str = Path(..., example=generate_dummy(type='pin_id')),user_id: str = Path(..., example=generate_dummy(type='user_id'))):
    try:
        return await hard_delete_pin_by_id(pin_id=id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.get("/api/v1/pin_trash/{user_id}", response_model=dict, 
    summary="Get all deleted pin (MySql)",
    description="This request is used to get all deleted pin based on given `user_id`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful fetch deleted pin",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "0c89ca34-09c2-08b9-2a73-a8935b9549d4",
                                "pin_name": "asdasdasasd",
                                "total_visit": 1,
                                "created_at": "2024-06-26T03:04:23",
                                "updated_at": "2024-07-13T02:32:53",
                                "deleted_at": "2024-10-01T02:40:37"
                            }
                        ],
                        "message": "Pin found",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found",
            "content": {
                "application/json": {
                    "example": {
                        "data": None,
                        "message": "Pin not found",
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
async def get_trash_pin_api(user_id: str = Path(..., example=generate_dummy(type='user_id'))):
    try:
        return await get_trash_pin(user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.put("/api/v1/pin/toggle_favorite/{id}/{user_id}", response_model=dict, 
    summary="Update pin favorite status / toggle (MySql)",
    description="This request is used to toggle pin favorite status based on given `user_id` and pin's`id`",
    tags=["Pin"],
    responses={
        200: {
            "description": "Successful update pin",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Pin updated",
                        "count": 1
                    }
                }
            }
        },
        404: {
            "description": "Pin not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Pin not found",
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
async def put_pin_favorite_api(user_id: str = Path(..., example=generate_dummy(type='user_id')),id: str = Path(..., example=generate_dummy(type='pin_id'))):
    try:
        return await put_pin_favorite(user_id=user_id,pin_id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_pin.post("/api/v1/pin", response_model=dict, 
    summary="Create a pin (MySql)",
    description="This request is used to create a new pin",
    tags=["Pin"],
    responses={
        201: {
            "description": "Successful created pin",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Pin created",
                        "data": {
                            "pin_name": "test 2 via api",
                            "pin_desc": "Tengah malam dan subuh ada portal. Tunggu depan warkop",
                            "pin_lat": "-6.237841118966224",
                            "pin_long": "106.85396032361263",
                            "pin_category": "Friend",
                            "pin_person": "Jhon Doe",
                            "pin_call": "08123456789",
                            "pin_email": "flazen.edu@gmail.com",
                            "pin_address": "Gatsu",
                            "is_favorite": 1,
                            "created_by": "fcd3f23e-e5aa-11ee-892a-3216422910e9",
                            "id": "c54ad278-396d-2a1f-03a2-eeb42bcb6d5d",
                            "created_at": "2024-10-21T03:11:52.257019"
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
        422: {
            "description": "Failed to validate the data",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Validation failed",
                        "errors": [
                            [
                                {
                                    "field": "Pin Latitude",
                                    "message": "Pin Latitude cant be empty"
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
async def post_pin_api(request : Request):
    try:
        data = await request.json()
        return await post_pin_query(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))