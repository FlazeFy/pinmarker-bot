from telegram import Update
from telegram.ext import CallbackContext
from timezonefinder import TimezoneFinder
tf = TimezoneFinder()
import pytz
from datetime import datetime

# Helpers
from helpers.sqlite.template import post_user_timezone

# Services
from bots.telegram.repositories.repo_user import api_get_profile_by_telegram_id
from bots.telegram.typography import send_long_message

# Repo
from bots.repositories.repo_pin import api_get_nearset_pin_share_loc

async def location_command(update: Update, context: CallbackContext) -> None:
    user_location = update.message.location
    latitude = user_location.latitude
    longitude = user_location.longitude

    # Timezone
    timezone_name = tf.timezone_at(lat=latitude, lng=longitude)

    if timezone_name:
        timezone_val = datetime.now(pytz.timezone(timezone_name))
        utc_offset = int(timezone_val.utcoffset().total_seconds() / 3600)

        userTeleId = update.message.from_user.id
        profile = await api_get_profile_by_telegram_id(teleId=userTeleId)

    if profile:
        userId = profile["data"]['id']
        username = "@"+profile["data"]["username"]
        post_user_timezone(socmed_id=userTeleId, socmed_platform='telegram', timezone=f"{'+' if utc_offset > 0 else '-'}{utc_offset}")
    else:
        username = update.message.from_user.username
        userId = None

    msg = f"Hello, {username} your location:\nLatitude: {latitude}\nLongitude: {longitude}\nTimezone: {timezone_name} UTC{'+' if utc_offset > 0 else '-'}{utc_offset}"
    await update.message.reply_text(msg)

    res = await api_get_nearset_pin_share_loc(userId=userId,max_dis=10000,lat=latitude,long=longitude)
    await update.message.reply_text(text=f"Showing {'global ' if not profile else ''}location...\n\n", parse_mode='HTML')
    message_chunks = send_long_message(res)
    for chunk in message_chunks:
        await update.message.reply_text(chunk, parse_mode='HTML')

    
