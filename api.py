from fastapi import FastAPI
from helpers.sqlite.template import init_db_sqlite
from services.modules.track.router import router_track
from services.modules.stats.router import router_stats
from services.modules.pin.router import router_pin
from services.modules.user.router import router_user
from services.modules.bot_history.router import router_bot_history
from services.modules.feedback.router import router_feedback
from services.modules.history.router import router_history
from services.modules.visit.router import router_visit
from services.modules.dictionary.router import router_dct
from services.modules.bot_relation.router import router_bot_relation
from services.modules.callback.line import router_callback_line
from fastapi.middleware.cors import CORSMiddleware
from bots.line import message_handler, location_handler

from configs.configs import cred
import firebase_admin

from services.scheduler.schedule import start_scheduler
app = FastAPI(
    title="PinMarker API",
    description="This is an Rest API documentation for all PinMarker request that used in PinMarker Mobile, PinMarker Telegram BOT, PinMarker Discord BOT, and PinMarker Web. This Backend environment was built using Fast API and have databases of MySQL, Firebase Realtime, and SQFlite for the database. And was hosted in CPanel.",
    version="1.0.0"
)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pinmarker-36552-default-rtdb.firebaseio.com/',
    'storageBucket': 'pinmarker-36552.appspot.com'
})
init_db_sqlite()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:2000",
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:2000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
app.include_router(router_track)
app.include_router(router_stats)
app.include_router(router_pin)
app.include_router(router_user)
app.include_router(router_bot_history)
app.include_router(router_feedback)
app.include_router(router_history)
app.include_router(router_visit)
app.include_router(router_dct)
app.include_router(router_callback_line)
app.include_router(router_bot_relation) 

@app.get("/")
async def root():
    return {"message": "Welcome to PinMarker"}

@app.on_event("startup")
def on_startup():
    start_scheduler()

__all__ = ['app']