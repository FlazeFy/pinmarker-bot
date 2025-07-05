import os
from dotenv import load_dotenv
import logging
logging.basicConfig(
    filename='line_message.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

load_dotenv()
IS_TEST_MODE = os.getenv("IS_TEST_MODE")

from linebot.models import TemplateSendMessage, MessageAction, CarouselColumn, CarouselTemplate, MessageEvent, TextMessage,TextSendMessage,LocationSendMessage
from services.modules.callback.line import line_bot_api

def get_sender_id(event):
    source_type = event.source.type

    if source_type == "group":
        senderId = event.source.group_id
    elif source_type == "user":
        senderId = event.source.user_id
    elif source_type == "room":
        senderId = event.source.room_id

    return senderId

def send_message_text(senderId, message: str):
    if IS_TEST_MODE == "false":
        line_bot_api.push_message(senderId, TextSendMessage(text=message))
    else:
        logging.info(f"[TEST] Message send to {senderId}: {message}")

def send_message_error(senderId, message: str):
    if IS_TEST_MODE == "false":
        line_bot_api.push_message(senderId, TextSendMessage(text="Error processing the response"))
    else:
        logging.info(f"[TEST] Message send to {senderId}: Error processing the response")

    logging.info(f"[ERROR] Message send to {senderId}: Error processing the response")

def send_location_text(senderId, title, address: str, lat, long):
    if IS_TEST_MODE == "false":
        line_bot_api.push_message(
            senderId,  
            LocationSendMessage(
                title=title,
                address=address,
                latitude=lat,
                longitude=long
            )
        )
    else:
        logging.info(f"[TEST MODE] Location send to {senderId}: title='{title}', address='{address}', lat={lat}, long={long}")
