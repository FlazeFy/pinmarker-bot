from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import io
import os

# Services
from services.modules.pin.pin_queries import get_all_pin
from services.modules.visit.visit_queries import get_all_visit_last_day, get_all_visit_csv
from services.modules.stats.stats_queries import get_dashboard, get_stats
from services.modules.stats.stats_capture import get_stats_capture
from services.modules.track.track_queries import get_last_tracker_position
from services.modules.user.user_queries import get_profile_by_telegram_id
from services.modules.user.user_command import update_sign_out
from helpers.telegram.repositories.repo_bot_history import api_get_command_history
from helpers.telegram.typography import send_long_message

async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Type your username : ')
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    userTeleId = query.from_user.id
    profile = await get_profile_by_telegram_id(teleId=userTeleId)

    if profile["is_found"]:
        userId = profile['data'].id
        role = profile['role']
        await query.answer()

        if query.data == '1':
            res = await get_all_pin(type='bot',userId=userId)
            message_chunks = send_long_message(res)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text="Showing location...", reply_markup=reply_markup, parse_mode='HTML')
            for chunk in message_chunks:
                await context.bot.send_message(chat_id=query.message.chat_id, text=chunk, parse_mode='HTML')
        
        # if query.data == '2':

        elif query.data == '3':
            res = await get_all_visit_last_day(userId=userId, teleId=userTeleId)
            message_chunks = send_long_message(res)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            for chunk in message_chunks:
                await context.bot.send_message(chat_id=query.message.chat_id, text=chunk, parse_mode='HTML')
            await context.bot.send_message(chat_id=query.message.chat_id, text="Please choose an option:", reply_markup=reply_markup)

        elif query.data == '3/csv':
            csv_content, file_name = await get_all_visit_csv(platform='telegram', userId=userId, teleId=userTeleId)
            if csv_content and file_name:
                file = io.BytesIO(csv_content.encode('utf-8'))
                file.name = file_name        
                keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_document(document=file, caption="Generate CSV file of history...\n\n", reply_markup=reply_markup)
            else:
                await query.edit_message_text(text=f"<i>- {file_name} -</i>", reply_markup= main_menu_keyboard(), parse_mode='HTML')

        elif query.data == '4':
            res = await get_dashboard(type='bot', userId=userId, role=role)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=f"Showing dashboard...\n\n", reply_markup=reply_markup, parse_mode='HTML')
            await query.edit_message_text(text=res, reply_markup=reply_markup, parse_mode='HTML')

        elif query.data == '5':
            res = await get_stats(userId=userId)
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

        elif query.data == '9':
            res, type, _ = await api_get_command_history(tele_id=userTeleId)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if type == 'file':
                await query.message.reply_document(document=res, caption="Generate CSV file of history...\n\n", reply_markup=reply_markup)
            elif type == 'text':
                await query.edit_message_text(text=f"Showing bot history...\n{res}\n", reply_markup=reply_markup, parse_mode='HTML')
            else:
                await query.edit_message_text(text=f"Error processing the response", reply_markup=reply_markup, parse_mode='HTML')

        elif query.data == '0':
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data='sign_out_yes')],
                [InlineKeyboardButton("No", callback_data='sign_out_no')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(text="Are you sure you want to sign out?",reply_markup=reply_markup)
        elif query.data == 'sign_out_yes':
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            res = await update_sign_out(userId=userId, teleId=userTeleId, role=role)
            await query.edit_message_text(res["message"], reply_markup=reply_markup)

        elif query.data == 'back' or query.data == 'sign_out_no':
            await query.edit_message_text(text='What do you want:', reply_markup= main_menu_keyboard())
    else:
        await query.edit_message_text(text='What do you want:', reply_markup= main_menu_keyboard())

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = main_menu_keyboard()
    userId = update.message.from_user.id
    profile = await get_profile_by_telegram_id(teleId=userId)

    if profile["is_found"]:
        username = profile["data"].username
        await update.message.reply_text(
            f"Hello @{username}, What do you want:\nOr send me your location to show your pin distance:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(profile["message"])
        await update.message.reply_text(f"\nYour Telegram ID : {userId}")

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Show my pin", callback_data='1')],
        [InlineKeyboardButton("Show detail pin", callback_data='2')],
        [InlineKeyboardButton("History visit", callback_data='3')],
        [InlineKeyboardButton("History visit in CSV ", callback_data='3/csv')],
        [InlineKeyboardButton("Dashboard", callback_data='4')],
        [InlineKeyboardButton("Stats", callback_data='5')],
        [InlineKeyboardButton("Change password", callback_data='6')],
        [InlineKeyboardButton("Last Live Tracker Position", callback_data='7')],
        [InlineKeyboardButton("- Send Feedback -", callback_data='8')],
        [InlineKeyboardButton("- BOT History -", callback_data='9')],
        [InlineKeyboardButton("- Help Center -", callback_data='10')],
        [InlineKeyboardButton("- About Us -", callback_data='11')],
        [InlineKeyboardButton("Exit Bot", callback_data='0')]
    ]
    return InlineKeyboardMarkup(keyboard)
