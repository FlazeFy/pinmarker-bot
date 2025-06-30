import asyncio
import threading
from linebot.models import TemplateSendMessage, MessageAction, CarouselColumn, CarouselTemplate, MessageEvent, TextMessage,TextSendMessage
from bots.telegram.typography import send_long_message
from configs.menu_list import MENU_LIST_USER, ABOUT_US
from services.modules.callback.line import line_bot_api, handler 

# Helper
from helpers.converter import strip_html_tags
from helpers.sqlite.template import post_ai_command
# Repo
from bots.repositories.repo_pin import api_get_all_pin

userId = "474f7c95-9387-91ad-1886-c97239b24992"

def chunk_buttons(buttons, chunk_size=3):
    chunks = [buttons[i:i + chunk_size] for i in range(0, len(buttons), chunk_size)]
    for chunk in chunks:
        while len(chunk) < chunk_size:
            chunk.append({"label": " ", "data": " "})
    return chunks

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    source_type = event.source.type
    message = event.message
    message_text = message.text.lower()

    if source_type == "group" or source_type == "room":
        if '/pinmarker' in message_text or 'pinmarker' in message_text:
            handle_menu(event)
        else:
            handle_command(event)
    elif source_type == "user":
        if '/start' in message_text:
            handle_menu(event)
        else:
            handle_command(event)
        
def handle_command(event):
    message = event.message
    source_type = event.source.type
    message_text = message.text.lower()

    if source_type == "group":
        senderId = event.source.group_id
    elif source_type == "user":
        senderId = event.source.user_id

    if message_text == "/show_my_pin":
        post_ai_command(socmed_id=senderId, socmed_platform='line',command=message_text)

        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                res, res_type, is_success, uploaded_link = loop.run_until_complete(api_get_all_pin(user_id=userId))
                
                if res_type == 'file':
                    line_bot_api.push_message(
                        senderId,
                        TextSendMessage(text=f"Generated file (CSV) is not supported to send directly. But you can access this uploaded file from my storage.\n\n{uploaded_link}")
                    )
                elif res_type == 'text':
                    message_chunks = send_long_message(f"Showing Location Data:\n\n{strip_html_tags(res)}")
                    for chunk in message_chunks:
                        line_bot_api.push_message(
                            senderId,
                            TextSendMessage(text=chunk)
                        )
                else:
                    line_bot_api.push_message(
                        senderId,
                        TextSendMessage(text="Error processing the response")
                    )
            finally:
                loop.close()

        threading.Thread(target=run_async).start()
    elif message_text == "/about_us":
        line_bot_api.push_message(
            senderId,
            TextSendMessage(text=ABOUT_US)
        )

def handle_menu(event):
    button_chunks = chunk_buttons(MENU_LIST_USER)

    columns = []
    for i, chunk in enumerate(button_chunks):
        actions = [MessageAction(label=btn["label"], text=btn["data"]) for btn in chunk]

        if i == 0:
            column = CarouselColumn(
                title="PinMarker Bot",
                text="Hello @[username], please choose an option :",
                actions=actions
            )
        else:
            column = CarouselColumn(
                title="PinMarker Bot",
                text="Choose an option :",
                actions=actions
            )

        columns.append(column)

    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text="Choose an option :",
            template=CarouselTemplate(columns=columns)
        )
    )
