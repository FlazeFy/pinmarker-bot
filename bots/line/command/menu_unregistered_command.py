from linebot.models import TemplateSendMessage, MessageAction, CarouselColumn, CarouselTemplate, MessageEvent, TextMessage
from configs.menu_list import GREETING_MSG, GREETING_UNKNOWN_USER_MSG, MENU_LIST_UNKNOWN_GROUP

# Services
from services.modules.callback.line import line_bot_api, handler 
# Helper
from bots.line.helper import chunk_buttons, get_sender_id, send_message_text

def menu_unregistered_command(event,source_type):
    senderId = get_sender_id(event)

    send_message_text(senderId, GREETING_MSG)
    send_message_text(senderId, GREETING_UNKNOWN_USER_MSG)

    if source_type == "group":
        button_chunks = chunk_buttons(MENU_LIST_UNKNOWN_GROUP)

    columns = []
    for _, chunk in enumerate(button_chunks):
        actions = [MessageAction(label=btn["label"], text=btn["data"]) for btn in chunk]
        columns.append(CarouselColumn(
            title="PinMarker Bot",
            text="Choose an option :",
            actions=actions
        ))

    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text="Choose an option :",
            template=CarouselTemplate(columns=columns)
        )
    )