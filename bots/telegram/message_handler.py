from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import os

# Services
from services.modules.stats.stats_queries import get_stats
from services.modules.stats.stats_capture import get_stats_capture
from services.modules.user.user_command import update_sign_out
# Helpers
from bots.repositories.repo_stats import api_get_dashboard
from bots.repositories.repo_user import api_get_profile_by_telegram_id
from bots.repositories.repo_visit import api_get_visit_history
from bots.telegram.typography import send_long_message
# Repo
from bots.repositories.repo_pin import api_get_all_pin, api_get_all_pin_name, api_get_all_pin_export
from bots.repositories.repo_track import api_get_last_track
from bots.repositories.repo_bot_history import api_get_command_history

from helpers.sqlite.query import post_ai_command
from configs.menu_list import MENU_LIST_USER,ABOUT_US

async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Type your username : ')
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    userTeleId = query.from_user.id
    profile = await api_get_profile_by_telegram_id(teleId=userTeleId)

    if profile["is_found"]:
        userId = profile['data']['id']
        role = profile['role']
        await query.answer()

        if query.data == '/show_my_pin':
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/Show my pin')
            res, type, is_success, _ = await api_get_all_pin(userId)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if type == 'file':
                await query.message.reply_document(document=res, caption="Generate CSV file of pin...\n\n", reply_markup=reply_markup)
            elif type == 'text':
                message_chunks = send_long_message(res)
                for chunk in message_chunks:
                    await context.bot.send_message(chat_id=query.message.chat_id, text=chunk, parse_mode='HTML')
            else:
                await query.edit_message_text(text=f"Error processing the response", reply_markup=reply_markup, parse_mode='HTML')      

        elif query.data == '/export_pins':
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/Export pin')
            res, is_success, _ = await api_get_all_pin_export(userId)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if is_success:
                if len(res) == 1:
                    await query.edit_message_text(text=f"Generate Exported CSV file of pin...", parse_mode='HTML')     
                else:     
                    await query.edit_message_text(text=f"Generate Exported CSV file of pin...\nSpliting into {len(res)} parts. Each of these have maximum 100 pin", parse_mode='HTML')     
                for idx, dt in enumerate(res):
                    await query.message.reply_document(document=dt, caption=f"Part-{idx+1}\n")
                await query.edit_message_text(text=f"Export finished", parse_mode='HTML',reply_markup= main_menu_keyboard(),)     
            else:
                await query.edit_message_text(text=f"<i>- {res} -</i>", reply_markup= main_menu_keyboard(), parse_mode='HTML')         
        
        elif query.data == '/pin_details':
            res = await api_get_all_pin_name(userId)
            message_chunks = send_long_message(res)
            for chunk in message_chunks:
                await context.bot.send_message(chat_id=query.message.chat_id, text=chunk, parse_mode='HTML')

        elif query.data == '/visit_last_30d' or query.data == '/all_visit_history':
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/History visit last 30 days')
            res, type, _ = await api_get_visit_history(userId, '30' if query.data == '/visit_last_30d' else 'all')
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if type == 'file':
                if len(res) == 1:
                    await query.edit_message_text(text=f"Generate Exported CSV file of visit history...", parse_mode='HTML')     
                else:     
                    await query.edit_message_text(text=f"Generate Exported CSV file of visit history...\nSpliting into {len(res)} parts. Each of these have maximum 100 history", parse_mode='HTML')     
                for idx, dt in enumerate(res):
                    await query.message.reply_document(document=dt, caption=f"Part-{idx+1}\n")
                await query.edit_message_text(text=f"Export finished", parse_mode='HTML',reply_markup= main_menu_keyboard(),)
            elif type == 'text':
                message_chunks = send_long_message(res)
                for chunk in message_chunks:
                    await context.bot.send_message(chat_id=query.message.chat_id, text=chunk, parse_mode='HTML',reply_markup=reply_markup)
            else:
                await query.edit_message_text(text=f"Error processing the response", reply_markup=reply_markup, parse_mode='HTML')   

        elif query.data == '/dashboard':
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/Dashboard')
            res, is_success = await api_get_dashboard(userId, role)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if is_success:
                await query.edit_message_text(text=f"Showing dashboard...\n{res}\n", reply_markup=reply_markup, parse_mode='HTML')
            else:
                await query.edit_message_text(text=f"Error processing the response", reply_markup=reply_markup, parse_mode='HTML')

        elif query.data == '/stats':
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/Stats')
            res = await get_stats(userId=userId)
            res_capture = await get_stats_capture()
            if res_capture:
                with open(res_capture, 'rb') as photo:
                    await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo)
                os.remove(res_capture)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=f"Showing stats...\n\n{res}", reply_markup=reply_markup, parse_mode='HTML')

        elif query.data == '/live_tracker':
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/Last Live Tracker Position')
            track_lat, track_long, msg, is_success = await api_get_last_track(userId)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if is_success:
                if track_lat is not None and track_long is not None:
                    await context.bot.send_location(chat_id=query.message.chat_id, latitude=track_lat, longitude=track_long)
                await query.edit_message_text(text=f"Showing last tracking...\n{msg}\n", reply_markup=reply_markup, parse_mode='HTML')
            else:
                await query.edit_message_text(text=f"Error processing the response", reply_markup=reply_markup, parse_mode='HTML')

        elif query.data == '/bot_history':
            res, type, _, _ = await api_get_command_history(userTeleId)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if type == 'file':
                await query.message.reply_document(document=res, caption="Generate CSV file of history...\n\n", reply_markup=reply_markup)
            elif type == 'text':
                await query.edit_message_text(text=f"Showing bot history...\n{res}\n", reply_markup=reply_markup, parse_mode='HTML')
            else:
                await query.edit_message_text(text=f"Error processing the response", reply_markup=reply_markup, parse_mode='HTML')

        elif query.data == '/about_us':
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=ABOUT_US, reply_markup=reply_markup)
            
        elif query.data == '/exit_bot':
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
    profile = await api_get_profile_by_telegram_id(teleId=userId)

    if profile["is_found"]:
        username = profile["data"]['username']
        await update.message.reply_text(
            f"Hello @{username}, What do you want:\nOr send me your location to show your pin distance:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(profile["message"])
        await update.message.reply_text(f"\nYour Telegram ID : {userId}")

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton(item["label"], callback_data=item["data"])]
        for item in MENU_LIST_USER
    ]
    return InlineKeyboardMarkup(keyboard)
