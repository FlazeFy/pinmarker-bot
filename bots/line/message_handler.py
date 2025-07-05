import asyncio
import threading
from linebot.models import TemplateSendMessage, MessageAction, CarouselColumn, CarouselTemplate, MessageEvent, TextMessage

# Config
from configs.menu_list import (
    ABOUT_US, ASK_NAME_REGISTER_MSG, DETECT_LINK, SIGN_OUT_GOOD_BYE,
    ASK_COORDINATE, THANKS_PIN_CREATE,ASK_PIN_NAME
)
# Services
from services.modules.callback.line import line_bot_api, handler 
# Helper
from helpers.validator import contains_link
from helpers.sqlite.query import post_ai_command
from bots.line.helper import chunk_buttons, get_sender_id, send_location_text, send_message_text, send_message_error
# Repo
from bots.repositories.repo_pin import api_post_create_pin
from bots.repositories.repo_bot_relation import api_post_check_bot_relation, api_post_create_bot_relation, api_post_sign_out_bot_relation
from bots.repositories.repo_dictionary import api_get_dictionary_by_type
# Command
from bots.line.command.menu_registered_command import menu_registered_command
from bots.line.command.menu_unregistered_command import menu_unregistered_command
from bots.line.command.bot_history_command import bot_history_command
from bots.line.command.dashboard_command import dashboard_command
from bots.line.command.export_pins_command import export_pins_command
from bots.line.command.live_tracker_command import live_tracker_command
from bots.line.command.pin_details_command import pin_details_command
from bots.line.command.show_my_pin_command import show_my_pin_command
from bots.line.command.visit_history_command import visit_history_command
# State Management
from bots.line.state_management import group_register_state, marker_create_state

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    source_type = event.source.type
    message_text = event.message.text.strip()
    senderId = get_sender_id(event)

    def run_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            keyword_start = (
                ('/pinmarker' in message_text.lower() or 'pinmarker' in message_text.lower())
                if source_type in ['group', 'room']
                else '/start' in message_text.lower()
            )
            is_contain_link = contains_link(message_text)

            # Repo : Check Bot Relation
            is_registered, err_check_relation, data_check_relation = loop.run_until_complete(api_post_check_bot_relation(senderId, source_type,'line'))

            # Handle Register State
            # Check if chat is waiting for a group name
            if group_register_state.get(senderId) == 'awaiting_group_name':
                groupName = message_text

                # Validator 
                if len(groupName) > 75:
                    send_message_text(senderId, "Group name must be under 75 characters 😢")
                    return
                if contains_link(groupName):
                    send_message_text(senderId, "Group name must not contain any link 😢")
                    return

                # Repo : Create Bot Relation
                loop.run_until_complete(api_post_create_bot_relation(senderId,groupName,source_type))
                send_message_text(senderId, f"Yay! you're now registered 🎉. Welcome to PinMarker, {groupName}")
                del group_register_state[senderId]
                return
            
            #   Marker Creation Flow
            user_state = marker_create_state.get(senderId)

            if isinstance(user_state, dict) and user_state.get('step') == 'awaiting_coordinate':
                parts = message_text.split(',')
                if len(parts) == 2:
                    try:
                        lat = float(parts[0].strip())
                        long = float(parts[1].strip())
                        marker_create_state[senderId]['step'] = 'awaiting_pin_name'
                        marker_create_state[senderId]['pin_lat'] = lat
                        marker_create_state[senderId]['pin_long'] = long
                        send_message_text(senderId, ASK_PIN_NAME)
                        return
                    except ValueError:
                        send_message_text(senderId, "Please send valid coordinates (e.g., '-6.2000, 106.8166')")
                        return
                else:
                    send_message_text(senderId, "Please send coordinates in the format: latitude, longitude")
                    return

            elif isinstance(user_state, dict) and user_state.get('step') == 'awaiting_pin_name':
                marker_create_state[senderId]['pin_name'] = message_text
                marker_create_state[senderId]['step'] = 'awaiting_category'

                if data_check_relation is not None:
                    # Repo : Get Dictionary (Pin Category By Type)
                    _, data = loop.run_until_complete(api_get_dictionary_by_type('pin_category', data_check_relation['created_by']))
                else:
                    send_message_error(senderId, err_check_relation)
                    return

                # Marker Creation Flow : Show category options via menu
                if data is not None:
                    columns_pin_category = []
                    for _, dt in enumerate(data):
                        columns_pin_category.append(
                            {"label": dt['dictionary_name'], "data": f"/category_{dt['dictionary_name'].replace(' ','_')}"}
                        )

                    button_chunks = chunk_buttons(columns_pin_category)
                    columns = []
                    for _, chunk in enumerate(button_chunks):
                        actions = [MessageAction(label=btn["label"], text=btn["data"]) for btn in chunk]
                        columns.append(CarouselColumn(
                            title="PinMarker Bot",
                            text="Choose a category :",
                            actions=actions
                        ))

                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text="Choose a category :",
                            template=CarouselTemplate(columns=columns)
                        )
                    )
                else:
                    send_message_error(senderId, msg)

            elif isinstance(user_state, dict) and user_state.get('step') == 'awaiting_category':
                if message_text.startswith("/category_"):
                    category = message_text.replace("category_", "").replace("/","")
                    category = category.replace("_", " ").title()
                    marker_create_state[senderId]['pin_category'] = category

                    if data_check_relation is not None:
                        # Repo: Create Marker
                        pin_lat = str(marker_create_state[senderId]['pin_lat'])
                        pin_long = str(marker_create_state[senderId]['pin_long'])
                        pin_desc = marker_create_state[senderId]['pin_desc']
                        pin_name = marker_create_state[senderId]['pin_name']
                        pin_address = marker_create_state[senderId].get('pin_address', None)
                        data = {
                            "pin_name": pin_name,
                            "pin_desc": pin_desc,
                            "pin_lat": pin_lat,
                            "pin_long": pin_long,
                            "pin_category": category,
                            "pin_address": pin_address,
                        }
                        msg, is_success = loop.run_until_complete(api_post_create_pin(data,data_check_relation['created_by']))

                        if is_success == True:
                            send_location_text(senderId, pin_name, pin_address if pin_address is not None else pin_desc, pin_lat, pin_long)
                            send_message_text(senderId, THANKS_PIN_CREATE)
                        elif is_success == False:
                            send_message_text(senderId, msg)
                        else:
                            send_message_error(senderId, msg)
                        del marker_create_state[senderId]
                        return
                    else:
                        send_message_error(senderId, err_check_relation)
                        return

            # Marker Creation Flow : Detect link to start marker creation
            if is_contain_link and group_register_state.get(senderId) != 'awaiting_group_name':
                if is_registered and err_check_relation is None:
                    send_message_text(senderId, DETECT_LINK)

                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text="Choose an option :",
                            template=CarouselTemplate(columns=[
                                CarouselColumn(
                                    title="Add a New Marker",
                                    text="Choose an option :",
                                    actions=[
                                        MessageAction(label="Yes, save it!", text="/yes_create_marker-via_link"),
                                        MessageAction(label="No, ignore this", text="/no_create_marker")
                                    ]
                                )
                            ])
                        )
                    )
                    if senderId not in marker_create_state:
                        marker_create_state[senderId] = {}

                    marker_create_state[senderId]['pin_desc'] = message_text
                    return
                elif not is_registered and err_check_relation is None:
                    return 
                else:
                    send_message_error(senderId, err_check_relation)
                    return 
                
            if message_text.startswith("/yes_create_marker"):
                if message_text == "/yes_create_marker-via_link":
                    send_message_text(senderId, ASK_COORDINATE)
                    if senderId not in marker_create_state:
                        marker_create_state[senderId] = {}
                    marker_create_state[senderId]['step'] = 'awaiting_coordinate'
                elif message_text == "/yes_create_marker-via_shareloc":
                    marker_create_state[senderId]['pin_desc'] = None
                    marker_create_state[senderId]['step'] = 'awaiting_pin_name'
                    send_message_text(senderId, ASK_PIN_NAME)
                else:
                    send_message_error(senderId, "Error processing the response")
                return

            if message_text == "/no_create_marker":
                send_message_text(senderId, "Okay, noted it 🫡")
                marker_create_state.pop(senderId, None)
                del marker_create_state[senderId]
                return
            
            # Sign Out Flow
            if message_text == "/yes_sign_out":
                # Repo : Sign Out Bot Relation
                is_success, err_sign_out = loop.run_until_complete(api_post_sign_out_bot_relation(senderId, source_type,'line'))

                if is_success == True:
                    send_message_text(senderId, SIGN_OUT_GOOD_BYE)
                elif is_success == False:
                    send_message_text(senderId, f"{err_check_relation}, account already sign out")
                else:
                    send_message_error(senderId, err_sign_out)
                return

            if message_text == "/no_sign_out":
                send_message_text(senderId, "Okay, noted it 🫡")
                return
            
            if message_text == "/register_group" and source_type in ['group', 'room']:
                group_register_state[senderId] = 'awaiting_group_name'
                send_message_text(senderId, ASK_NAME_REGISTER_MSG)
                return

            # Start Command
            if keyword_start and not is_contain_link:
                # Define Menu
                if err_check_relation is None:
                    if is_registered:
                        if keyword_start:
                            menu_registered_command(event, source_type, data_check_relation)
                        else:
                            handle_command(event, data_check_relation)
                    else:
                        menu_unregistered_command(event, source_type)
                else: 
                    send_message_error(senderId, err_check_relation)
            elif not is_contain_link:
                handle_command(event, data_check_relation)

        except Exception as e:
            send_message_error(senderId, str(e))
        finally:
            loop.close()

    threading.Thread(target=run_async).start()
        
def handle_command(event, data):
    message = event.message
    message_text = message.text.lower()
    senderId = get_sender_id(event)
    userId = data['created_by']
    username = data['username']

    if not any(x in message_text for x in ["/about_us", "/pin_details", "/bot_history"]):
        post_ai_command(socmed_id=senderId, socmed_platform='line',command=message_text)

    if message_text == "/show_my_pin":
        threading.Thread(target=show_my_pin_command, args=(senderId, userId)).start()

    elif message_text == "/export_pins":
        threading.Thread(target=export_pins_command, args=(senderId, userId)).start()

    elif message_text == "/dashboard":
        threading.Thread(target=dashboard_command, args=(senderId, userId)).start()

    elif message_text == "/about_us":
        send_message_text(senderId, ABOUT_US)

    elif message_text == "/pin_details":
        threading.Thread(target=pin_details_command, args=(senderId, userId,)).start()

    elif message_text == "/visit_last_30d" or message_text == "/all_visit_history":
        threading.Thread(target=visit_history_command, args=(senderId, userId, message_text,)).start()

    elif message_text == "/live_tracker":
        threading.Thread(target=live_tracker_command, args=(senderId, userId,)).start()

    elif message_text == "/bot_history":
        threading.Thread(target=bot_history_command, args=(senderId,)).start()

    elif message_text == "/exit_bot":
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="Choose an option :",
                template=CarouselTemplate(columns=[
                    CarouselColumn(
                        title="Are you sure?",
                        text=f"Choose an option to sign out from {username}'s account:",
                        actions=[
                            MessageAction(label="Yes, Sign out", text="/yes_sign_out"),
                            MessageAction(label="Maybe later", text="/no_sign_out")
                        ]
                    )
                ])
            )
        )

