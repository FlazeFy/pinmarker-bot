from services.modules.history.model import history 
from configs.configs import db
from sqlalchemy import select
from fastapi.responses import JSONResponse
    
async def get_all_history(userId:str):
    # Query builder
    query = select(
        history.c.id,
        history.c.history_type,
        history.c.history_context,
        history.c.created_at
    ).where(
        history.c.created_by == userId,
    ).order_by(
        history.c.created_at.desc()
    )

    # Exec
    result = db.connect().execute(query)
    data = result.fetchall()
    db.connect().close()

    data_list = [dict(row._mapping) for row in data]

    if len(data) > 0:
        data_list_final = []
        for row in data:
            data_list = dict(row._mapping)
            data_list['created_at'] = data_list['created_at'].isoformat() 
            data_list_final.append(data_list)
        data_list = data_list_final

        return JSONResponse(
            status_code=200, 
            content={
                "data": data_list,
                "message": "History found",
                "count": len(data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "History not found",
                "count": 0
            }
        )