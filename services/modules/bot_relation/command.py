from datetime import datetime, timedelta
from sqlalchemy import select, and_, insert
from fastapi.responses import JSONResponse
# Config
from configs.const import RELATION_PLATFORM, RELATION_TYPE
from configs.configs import db
# Helper
from helpers.validator import contains_item
from helpers.generator import get_UUID
# Model
from services.modules.bot_relation.model import bot_relation
from services.modules.user.user_model import user

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
            bot_relation.c.created_by,
            bot_relation.c.expired_at,
            user.c.username,
            user.c.email,
        ).join(
            user, user.c.id == bot_relation.c.created_by
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

async def post_create_bot_relation(data:dict):
    try:
        context_id = data.get('context_id')
        relation_type = data.get('relation_type')
        relation_platform = data.get('relation_platform')
        relation_name = data.get('relation_name')

        # Validator
        if not contains_item(relation_type,RELATION_TYPE):
            return JSONResponse(status_code=422, content={"message": "relation type is not valid"})
        if not contains_item(relation_platform,RELATION_PLATFORM):
            return JSONResponse(status_code=422, content={"message": "relation platform is not valid"})
        if not isinstance(relation_name, str) or relation_name == "" or len(relation_name) > 75:
            return JSONResponse(status_code=422, content={"message": "relation name is not valid"})

        created_at = datetime.utcnow()
        if relation_type == "user":
            expired_at = created_at + timedelta(days=60)
        elif relation_type == "group" or relation_type == "room": 
            expired_at = created_at + timedelta(days=30)

        id = get_UUID()
        query = insert(bot_relation).values(
            id=id,
            context_id=context_id,
            relation_type=relation_type,
            relation_platform=relation_platform,
            relation_name=relation_name,
            created_at=created_at,
            expired_at=expired_at
        )

        with db.connect() as conn:
            result = conn.execute(query)
            conn.commit()

        if result.rowcount > 0:
            return JSONResponse(
                status_code=201, 
                content={
                    "message": "Relation created",
                    "id": id,
                }
            )
        else:
            return JSONResponse(
                status_code=500, 
                content={
                    "message": "Something went wrong"
                }
            )
    except Exception as e:
        db.connect().rollback()
        raise

async def sign_out_bot_relation(data: dict):
    try:
        context_id = data.get('context_id')
        relation_type = data.get('relation_type')
        relation_platform = data.get('relation_platform')

        # Validator
        if not contains_item(relation_type, RELATION_TYPE):
            return JSONResponse(status_code=422, content={"message": "relation type is not valid"})
        if not contains_item(relation_platform, RELATION_PLATFORM):
            return JSONResponse(status_code=422, content={"message": "relation platform is not valid"})

        # Query builder
        delete_query = bot_relation.delete().where(
            and_(
                bot_relation.c.context_id == context_id,
                bot_relation.c.relation_type == relation_type,
                bot_relation.c.relation_platform == relation_platform,
            )
        )

        conn = db.connect()
        result = conn.execute(delete_query)
        conn.commit()
        conn.close()

        if result.rowcount > 0:
            return JSONResponse(
                status_code=200,
                content={"message": "Relation deleted"}
            )
        else:
            return JSONResponse(
                status_code=404,
                content={"message": "Relation not found"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={
                "message": "Something went wrong"
            }
        )
