from fastapi import FastAPI
from services.modules.track.router import router_track
from services.modules.stats.router import router_stats
from services.modules.pin.router import router_pin
from services.modules.user.router import router_user
from services.modules.bot_history.router import router_bot_history
from fastapi.middleware.cors import CORSMiddleware

from configs.configs import cred
import firebase_admin
app = FastAPI()
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pinmarker-36552-default-rtdb.firebaseio.com/',
    'storageBucket': 'pinmarker-36552.appspot.com'
})

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

@app.get("/")
async def root():
    return {"message": "Welcome to PinMarker"}

__all__ = ['app']