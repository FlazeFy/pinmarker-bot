from linebot.models import MessageEvent, TextMessage
from linebot.models import TemplateSendMessage, MessageAction, CarouselColumn, CarouselTemplate
from configs.menu_list import MENU_LIST_USER
from services.modules.callback.line import line_bot_api, handler 

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
    elif source_type == "user":
        if '/start' in message_text:
            handle_menu(event)

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
