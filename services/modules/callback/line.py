from fastapi import APIRouter, Request, Header, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import os
from dotenv import load_dotenv

load_dotenv()
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

router_callback_line = APIRouter()

@router_callback_line.post("/api/v1/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body_text = body.decode("utf-8")

    try:
        handler.handle(body_text, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return {"status": "ok"}
