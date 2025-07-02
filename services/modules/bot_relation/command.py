from services.modules.bot_relation.model import bot_relation
from configs.configs import db
from sqlalchemy import select, and_
from fastapi.responses import JSONResponse
# Config
from configs.const import RELATION_PLATFORM, RELATION_TYPE
# Helper
from helpers.validator import contains_item

async def post_check_bot_relation(data:dict):
    try:
        context_id = data.get('context_id')
        relation_type = data.get('relation_type')
        relation_platform = data.get('relation_platform')

        # Validator
        if not contains_item(relation_type,RELATION_TYPE):
            return JSONResponse(status_code=422, content={"message": "relation type is not valid"})
        if not contains_item(relation_platform,RELATION_PLATFORM):
            return JSONResponse(status_code=422, content={"message": "relation platform is not valid"})

        # Query builder
        query = select(
            bot_relation.c.context_id,
            bot_relation.c.relation_type,
            bot_relation.c.relation_platform,
            bot_relation.c.relation_name,
            bot_relation.c.created_at,
            bot_relation.c.expired_at
        ).where(
            and_(
                bot_relation.c.context_id == context_id,
                bot_relation.c.relation_type == relation_type,
                bot_relation.c.relation_platform == relation_platform,
            )
        )

        # Exec
        result = db.connect().execute(query)
        data = result.first()
        db.connect().close()

        if data:
            data = dict(data._mapping)
            data['created_at'] = data['created_at'].isoformat()
            if data['expired_at']:
                data['expired_at'] = data['expired_at'].isoformat()

            return JSONResponse(
                status_code=200, 
                content={
                    "data": data,
                    "message": "Relation checked",
                }
            )
        else:
            return JSONResponse(
                status_code=404, 
                content={
                    "message": "Relation not found",
                }
            )
    except Exception as e:
        db.connect().rollback()
        raise