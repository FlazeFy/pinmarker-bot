from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from services.modules.pin.pin_queries import get_pin_distance_by_coor

async def location_command(update: Update, context: CallbackContext) -> None:
    user_location = update.message.location
    latitude = user_location.latitude
    longitude = user_location.longitude
    
    msg = f"Your location:\nLatitude: {latitude}\nLongitude: {longitude}"
    await update.message.reply_text(msg)

    res = await get_pin_distance_by_coor(f"{latitude},{longitude}")
    keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=f"Showing location...\n\n{res}", reply_markup=reply_markup, parse_mode='HTML')
