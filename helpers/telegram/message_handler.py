from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import io
import os

# Services
from services.modules.pin.pin_queries import get_all_pin, get_all_pin_name, get_detail_pin
from services.modules.visit.visit_queries import get_all_visit, get_all_visit_csv
from services.modules.stats.stats_queries import get_dashboard, get_stats
from services.modules.stats.stats_capture import get_stats_capture
from services.modules.track.track_queries import get_last_tracker_position
from helpers.telegram.typography import send_long_message

async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Type your username : ')
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Handle different button presses here
    if query.data == '1':
        res = await get_all_pin(type='bot')
        message_chunks = send_long_message(res)
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Showing location...", reply_markup=reply_markup, parse_mode='HTML')
        for chunk in message_chunks:
            await context.bot.send_message(chat_id=query.message.chat_id, text=chunk, parse_mode='HTML')
        res = await get_all_pin_name()
        keyboard = []
        for dt in res:
            keyboard.append([InlineKeyboardButton(dt.pin_name, callback_data='detail_pin_'+dt.id)])
            
        keyboard.append([InlineKeyboardButton("Back", callback_data='back')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing location...", reply_markup=reply_markup)
    elif query.data.startswith('detail_pin_'):
        pin_id = query.data.split('_')[2]
        res, pin_lat, pin_long = await get_detail_pin(pin_id)
        if pin_lat is not None and pin_long is not None:
            await context.bot.send_location(chat_id=query.message.chat_id, latitude=pin_lat, longitude=pin_long)
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Pin opened...\n\n{res}", reply_markup=reply_markup, parse_mode='HTML')
    elif query.data == '3':
        res = await get_all_visit()
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing history...\n\n{res}", reply_markup=reply_markup, parse_mode='HTML')
    elif query.data == '3/csv':
        csv_content, file_name = await get_all_visit_csv(platform='telegram')
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = file_name        
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_document(document=file, caption="Generate CSV file of history...\n\n", reply_markup=reply_markup)
    elif query.data == '4':
        res = await get_dashboard(type='bot')
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing dashboard...\n\n{res}", reply_markup=reply_markup, parse_mode='HTML')
    elif query.data == '5':
        res = await get_stats()
        res_capture = await get_stats_capture()
        if res_capture:
            with open(res_capture, 'rb') as photo:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo)
            os.remove(res_capture)
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing stats...\n\n{res}", reply_markup=reply_markup, parse_mode='HTML')
    elif query.data == '6':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Preparing field...\n", reply_markup=reply_markup)
    elif query.data == '7':
        track_lat, track_long, msg = await get_last_tracker_position()
        if track_lat is not None and track_long is not None:
            await context.bot.send_location(chat_id=query.message.chat_id, latitude=track_lat, longitude=track_long)
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing last track position...\n{msg}\n", reply_markup=reply_markup, parse_mode='HTML')
    elif query.data == 'back':
        await query.edit_message_text(text='What do you want:', reply_markup= main_menu_keyboard())

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = main_menu_keyboard()
    await update.message.reply_text('What do you want:\nOr send my your location to show your pin distance :', reply_markup=reply_markup)

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("1. Show my pin", callback_data='1')],
        [InlineKeyboardButton("2. Show detail pin", callback_data='2')],
        [InlineKeyboardButton("3. History visit", callback_data='3')],
        [InlineKeyboardButton("3.1 History visit in CSV ", callback_data='3/csv')],
        [InlineKeyboardButton("4. Dashboard", callback_data='4')],
        [InlineKeyboardButton("5. Stats", callback_data='5')],
        [InlineKeyboardButton("6. Change password", callback_data='6')],
        [InlineKeyboardButton("7. Last Live Tracker Position", callback_data='7')],
        [InlineKeyboardButton("0. Exit bot", callback_data='0')]
    ]
    return InlineKeyboardMarkup(keyboard)
