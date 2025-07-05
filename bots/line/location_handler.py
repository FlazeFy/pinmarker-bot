import asyncio
import threading
from linebot.models import MessageEvent, LocationMessage
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()
from datetime import datetime
import pytz
# Helper
from helpers.converter import strip_html_tags
from bots.line.helper import send_message_text
# Services
from services.modules.callback.line import handler 
# Repo
from bots.repositories.repo_pin import api_get_nearset_pin_share_loc
# Repository
from bots.repositories.repo_bot_relation import api_post_check_bot_relation

@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    source_type = event.source.type
    latitude = event.message.latitude
    longitude = event.message.longitude
    address = event.message.address if event.message.address else "Unknown location"
    senderId = event.reply_token

    # Timezone
    timezone_name = tf.timezone_at(lat=latitude, lng=longitude)
    if timezone_name:
        timezone_val = datetime.now(pytz.timezone(timezone_name))
        utc_offset = int(timezone_val.utcoffset().total_seconds() / 3600)

    def run_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Repo : Check Bot Relation
            is_registered, err, data = loop.run_until_complete(api_post_check_bot_relation(senderId, source_type, 'line'))

            if is_registered:
                username = data['username']
                userId = data['created_by']
                msg = f"Hello {username}, your location:\nLatitude: {latitude}\nLongitude: {longitude}\nTimezone: {timezone_name} UTC{'+' if utc_offset > 0 else '-'}{utc_offset}\nAddress: {address}"
                send_message_text(senderId, msg)

                def run_async():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        res = loop.run_until_complete(
                            api_get_nearset_pin_share_loc(
                                userId=userId,
                                max_dis=10000,
                                lat=latitude,
                                long=longitude
                            )
                        )

                        if source_type == "group":
                            senderId = event.source.group_id
                        elif source_type == "user":
                            senderId = event.source.user_id
                            
                        send_message_text(senderId, f"Showing your nearest marked location...\n\n{strip_html_tags(res)}")
                    finally:
                        loop.close()

                threading.Thread(target=run_async).start()
            else:
                msg = f"Hello, your location:\nLatitude: {latitude}\nLongitude: {longitude}\nTimezone: {timezone_name} UTC{'+' if utc_offset > 0 else '-'}{utc_offset}\nAddress: {address}"
                send_message_text(senderId, msg)               

        except Exception as e:
            send_message_text(senderId, "Error processing the response")
        finally:
            loop.close()

    threading.Thread(target=run_async).start()
