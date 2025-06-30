import asyncio
import threading
from linebot.models import MessageEvent, LocationMessage, TextSendMessage
from timezonefinder import TimezoneFinder
tf = TimezoneFinder()
from datetime import datetime
import pytz

# Helper
from helpers.converter import strip_html_tags

# Services
from services.modules.callback.line import line_bot_api, handler 

# Repo
from bots.repositories.repo_pin import api_get_nearset_pin_share_loc

userId = "474f7c95-9387-91ad-1886-c97239b24992"

@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    source_type = event.source.type
    latitude = event.message.latitude
    longitude = event.message.longitude
    address = event.message.address if event.message.address else "Unknown location"

    # Timezone
    timezone_name = tf.timezone_at(lat=latitude, lng=longitude)
    if timezone_name:
        timezone_val = datetime.now(pytz.timezone(timezone_name))
        utc_offset = int(timezone_val.utcoffset().total_seconds() / 3600)

    msg = f"Hello, [username] your location:\nLatitude: {latitude}\nLongitude: {longitude}\nTimezone: {timezone_name} UTC{'+' if utc_offset > 0 else '-'}{utc_offset}\nAddress: {address}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )

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
                
            line_bot_api.push_message(
                senderId,
                TextSendMessage(text=f"Showing location...\n\n{strip_html_tags(res)}")
            )
        finally:
            loop.close()

    threading.Thread(target=run_async).start()

