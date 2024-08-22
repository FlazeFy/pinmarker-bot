from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import io
import os

# Services
from services.modules.pin.pin_queries import get_all_pin
from services.modules.visit.visit_queries import get_all_visit_last_day, get_all_visit_csv
from services.modules.stats.stats_queries import get_stats
from services.modules.stats.stats_capture import get_stats_capture
from services.modules.user.user_queries import get_profile_by_telegram_id
from services.modules.user.user_command import update_sign_out

# Helpers
from helpers.telegram.repositories.repo_bot_history import api_get_command_history
from helpers.telegram.repositories.repo_stats import api_get_dashboard
from helpers.telegram.repositories.repo_track import api_get_last_track
from helpers.telegram.repositories.repo_pin import api_get_all_pin, api_get_all_pin_export
from helpers.telegram.typography import send_long_message
from helpers.sqlite.template import post_ai_command

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
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/Show my pin')
            res, type, is_success = await api_get_all_pin(user_id=userId)
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

        elif query.data == '1/export':
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/Export pin')
            res, is_success = await api_get_all_pin_export(user_id=userId)
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
        
        # if query.data == '2':

        elif query.data == '3':
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/History visit')
            res = await get_all_visit_last_day(userId=userId, teleId=userTeleId)
            message_chunks = send_long_message(res)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            for chunk in message_chunks:
                await context.bot.send_message(chat_id=query.message.chat_id, text=chunk, parse_mode='HTML')
            await context.bot.send_message(chat_id=query.message.chat_id, text="Please choose an option:", reply_markup=reply_markup)

        elif query.data == '3/csv':
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/History visit in csv')
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
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/Dashboard')
            res, is_success = await api_get_dashboard(tele_id=userId, role=role)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if is_success:
                await query.edit_message_text(text=f"Showing dashboard...\n{res}\n", reply_markup=reply_markup, parse_mode='HTML')
            else:
                await query.edit_message_text(text=f"Error processing the response", reply_markup=reply_markup, parse_mode='HTML')

        elif query.data == '5':
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

        elif query.data == '6':
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=f"Preparing field...\n", reply_markup=reply_markup)

        elif query.data == '7':
            post_ai_command(socmed_id=userTeleId, socmed_platform='telegram',command='/Last Live Tracker Position')
            track_lat, track_long, msg, is_success = await api_get_last_track(user_id=userId)
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if is_success:
                if track_lat is not None and track_long is not None:
                    await context.bot.send_location(chat_id=query.message.chat_id, latitude=track_lat, longitude=track_long)
                await query.edit_message_text(text=f"Showing last tracking...\n{msg}\n", reply_markup=reply_markup, parse_mode='HTML')
            else:
                await query.edit_message_text(text=f"Error processing the response", reply_markup=reply_markup, parse_mode='HTML')

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

        elif query.data == '11':
            keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=f"PinMarker is an apps that store data about marked location on your maps. You can save location and separate it based on category or list. You can collaborate and share your saved location with all people. We also provide stats so you can monitoring your saved location.\n\nWe available on\nWeb : https://pinmarker.leonardhors.com/\n Telegram BOT : @Pinmarker_bot\nDiscord BOT : \nMobile Apps : \n\nParts of FlazenApps", reply_markup=reply_markup)
            
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
        [InlineKeyboardButton("Export pin", callback_data='1/export')],
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
