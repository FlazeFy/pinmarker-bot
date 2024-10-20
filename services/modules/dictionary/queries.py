from services.modules.dictionary.model import dictionary
from configs.configs import db
from sqlalchemy import select, and_, or_
from fastapi.responses import JSONResponse

async def get_all_dct_by_type_query(user_id:str, dct_type:str):
    # Query builder
    query = select(
        dictionary.c.dictionary_name,
        dictionary.c.dictionary_color
    ).where(
        or_(
            and_(
                dictionary.c.created_by == user_id,
                dictionary.c.dictionary_type == dct_type
            ),
            and_(
                dictionary.c.created_by.is_(None),
                dictionary.c.dictionary_type == dct_type
            )
        )
    ).order_by(
        dictionary.c.dictionary_name.asc()
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    if len(data) > 0:
        data = [dict(row._mapping) for row in data]
        return JSONResponse(
            status_code=200, 
            content={
                "data": data,
                "message": "Dictionary found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "Dictionary not found",
                "count": 0
            }
        )