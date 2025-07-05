from linebot.models import TemplateSendMessage, MessageAction, CarouselColumn, CarouselTemplate

# Config
from configs.menu_list import MENU_LIST_USER
# Services
from services.modules.callback.line import line_bot_api
# Helper
from bots.line.helper import chunk_buttons

def menu_registered_command(event,source_type,data):
    button_chunks = chunk_buttons(MENU_LIST_USER)
    username = data['username']

    columns = []
    for i, chunk in enumerate(button_chunks):
        actions = [MessageAction(label=btn["label"], text=btn["data"]) for btn in chunk]

        if i == 0:
            column = CarouselColumn(title="PinMarker Bot",text=f"Hello @{username}, please choose an option :",actions=actions)
        else:
            column = CarouselColumn(title="PinMarker Bot", text="Choose an option :", actions=actions)

        columns.append(column)

    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text="Choose an option :",
            template=CarouselTemplate(columns=columns)
        )
    )