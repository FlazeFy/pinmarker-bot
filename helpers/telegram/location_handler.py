from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from timezonefinder import TimezoneFinder
tf = TimezoneFinder()
import pytz
from datetime import datetime

# Helpers
from helpers.sqlite.template import post_user_timezone

# Services
from services.modules.pin.pin_queries import get_pin_distance_by_coor
from services.modules.user.user_queries import get_profile_by_telegram_id

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
        profile = await get_profile_by_telegram_id(teleId=userTeleId)

    if profile["is_found"]:
        userId = profile['data'].id
        username = "@"+profile["data"].username+" "
        post_user_timezone(socmed_id=userTeleId, socmed_platform='telegram', timezone=f"{'+' if utc_offset > 0 else '-'}{utc_offset}")
    else:
        username = ""

    msg = f"Hello, {username}your location:\nLatitude: {latitude}\nLongitude: {longitude}\nTimezone: {timezone_name} UTC{'+' if utc_offset > 0 else '-'}{utc_offset}"
    await update.message.reply_text(msg)

    res = await get_pin_distance_by_coor(f"{latitude},{longitude}",userId=userId)
    await update.message.reply_text(text=f"Showing location...\n\n{res}", parse_mode='HTML')

    
