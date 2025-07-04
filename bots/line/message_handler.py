import asyncio
import threading
from linebot.models import TemplateSendMessage, MessageAction, CarouselColumn, CarouselTemplate, MessageEvent, TextMessage

from bots.telegram.typography import send_long_message
# Config
from configs.menu_list import MENU_LIST_USER, ABOUT_US, MENU_LIST_UNKNOWN_GROUP, GREETING_MSG, GREETING_UNKNOWN_USER_MSG, ASK_NAME_REGISTER_MSG
# Services
from services.modules.callback.line import line_bot_api, handler 
# Helper
from helpers.converter import strip_html_tags
from helpers.sqlite.template import post_ai_command
from bots.line.helper import get_sender_id, send_message_text, send_location_text
# Repo
from bots.repositories.repo_pin import api_get_all_pin, api_get_all_pin_name, api_get_all_pin_export
from bots.repositories.repo_bot_history import api_get_command_history
from bots.repositories.repo_track import api_get_last_track
from bots.repositories.repo_visit import api_get_visit_history
from bots.repositories.repo_stats import api_get_dashboard
from bots.repositories.repo_bot_relation import api_post_check_bot_relation, api_post_create_bot_relation

group_register_state = {}

def chunk_buttons(buttons, chunk_size=3):
    chunks = [buttons[i:i + chunk_size] for i in range(0, len(buttons), chunk_size)]
    for chunk in chunks:
        while len(chunk) < chunk_size:
            chunk.append({"label": " ", "data": " "})
    return chunks

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    source_type = event.source.type
    message_text = event.message.text.strip()
    senderId = get_sender_id(event)

    def run_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Check if this chat is waiting for a group name
            if group_register_state.get(senderId) == 'awaiting_group_name':
                groupName = message_text

                # Validator
                if len(groupName) > 75:
                    send_message_text(senderId, "Group name must be under 75 characters 😢")
                    return

                # Repo : Create Bot Relation
                loop.run_until_complete(api_post_create_bot_relation(senderId,groupName,source_type))
                send_message_text(senderId, f"Yay! you're now registered 🎉. Welcome to PinMarker, {groupName}")
                del group_register_state[senderId]
                return

            # Repo : Check Bot Relation
            is_registered, err, data = loop.run_until_complete(api_post_check_bot_relation(senderId, source_type))

            keyword_triggered = (
                ('/pinmarker' in message_text.lower() or 'pinmarker' in message_text.lower())
                if source_type in ['group', 'room']
                else '/start' in message_text.lower()
            )

            # Define Menu
            if is_registered:
                if keyword_triggered:
                    handle_menu_registered(event, source_type, data)
                else:
                    handle_command(event, data)
            else:
                if message_text == "/register_group" and source_type in ['group', 'room']:
                    group_register_state[senderId] = 'awaiting_group_name'
                    send_message_text(senderId, ASK_NAME_REGISTER_MSG)
                else:
                    handle_menu_unregistered(event, source_type)

        except Exception as e:
            send_message_text(senderId, "Error processing the response")
        finally:
            loop.close()

    threading.Thread(target=run_async).start()
        
def handle_command(event, data):
    message = event.message
    message_text = message.text.lower()
    senderId = get_sender_id(event)
    userId = data['created_by']

    if not any(x in message_text for x in ["/about_us", "/pin_details", "/bot_history"]):
        post_ai_command(socmed_id=senderId, socmed_platform='line',command=message_text)

    if message_text == "/show_my_pin":
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                res, res_type, is_success, uploaded_link = loop.run_until_complete(api_get_all_pin(user_id=userId))
                
                if res_type == 'file' and is_success:
                    send_message_text(senderId, f"Generated file (CSV) is not supported to send directly. But you can access this uploaded file from my storage.\n\n{uploaded_link}")
                elif res_type == 'text' and is_success:
                    message_chunks = send_long_message(f"Showing Location Data:\n\n{strip_html_tags(res)}")
                    for chunk in message_chunks:
                        send_message_text(senderId, chunk)
                else:
                    send_message_text(senderId, "Error processing the response")
            finally:
                loop.close()

        threading.Thread(target=run_async).start()

    elif message_text == "/export_pins":
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                msg, _, uploaded_link = loop.run_until_complete(api_get_all_pin_export(user_id=userId))
                
                if uploaded_link is not None:
                    uploaded_link_str = ''
                    for idx, dt in enumerate(uploaded_link, start=1):
                        uploaded_link_str += f'Part-{idx}\n{dt}\n\n'

                    send_message_text(senderId, f"Generated file (CSV) is not supported to send directly. But you can access this uploaded file from my storage.\n\n{uploaded_link_str}")
                else:
                    send_message_text(senderId, msg)
            finally:
                loop.close()

        threading.Thread(target=run_async).start()

    elif message_text == "/dashboard":
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                res, is_success = loop.run_until_complete(api_get_dashboard(user_id=userId))
                
                if is_success is not None:
                    send_message_text(senderId, f"Showing dashboard...\n{res}\n")
                else:
                    send_message_text(senderId, res)
            finally:
                loop.close()

        threading.Thread(target=run_async).start()

    elif message_text == "/about_us":
        send_message_text(senderId, ABOUT_US)

    elif message_text == "/pin_details":
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                res = loop.run_until_complete(api_get_all_pin_name(userId))
                
                message_chunks = send_long_message(strip_html_tags(res))
                for chunk in message_chunks:
                    send_message_text(senderId, chunk)
            finally:
                loop.close()

        threading.Thread(target=run_async).start()

    elif message_text == "/visit_last_30d" or message_text == "/all_visit_history":
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                res, type, uploaded_link = loop.run_until_complete(api_get_visit_history(userId, '30' if message_text == '/visit_last_30d' else 'all'))
                
                if type == 'file':
                    uploaded_link_str = ''
                    for idx, dt in enumerate(uploaded_link, start=1):
                        uploaded_link_str += f'Part-{idx}\n{dt}\n\n'

                    send_message_text(senderId, f"Generated file (CSV) is not supported to send directly. But you can access this uploaded file from my storage.\n\n{uploaded_link_str}")
                elif type == 'text':
                    message_chunks = send_long_message(strip_html_tags(res))
                    for chunk in message_chunks:
                        send_message_text(senderId, chunk)
                else:
                    send_message_text(senderId, "Error processing the response")
            finally:
                loop.close()

        threading.Thread(target=run_async).start()

    elif message_text == "/live_tracker":
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                track_lat, track_long, msg, is_success = loop.run_until_complete(api_get_last_track(userId))
                
                if is_success:
                    send_message_text(senderId, f"Showing last tracking...\n{msg}")

                    if track_lat is not None and track_long is not None:
                        coor = f'{track_lat}, {track_long}'
                        send_location_text(senderId, 'Live Tracker Position', coor, track_lat, track_long)
                else:
                    send_message_text(senderId, "Error processing the response")
            finally:
                loop.close()

        threading.Thread(target=run_async).start()

    elif message_text == "/bot_history":
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                res, res_type, is_success, uploaded_link = loop.run_until_complete(api_get_command_history(senderId))
                
                if res_type == 'file' and is_success:
                    send_message_text(senderId, f"Generated file (CSV) is not supported to send directly. But you can access this uploaded file from my storage.\n\n{uploaded_link}")
                elif res_type == 'text' and is_success:
                    message_chunks = send_long_message(f"Showing bot history...\n\n{strip_html_tags(res)}")
                    for chunk in message_chunks:
                        send_message_text(senderId, chunk)
                else:
                    send_message_text(senderId, "Error processing the response")
            finally:
                loop.close()

        threading.Thread(target=run_async).start()

def handle_menu_registered(event,source_type,data):
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

def handle_menu_unregistered(event,source_type):
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

