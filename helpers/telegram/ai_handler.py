import nltk
from nltk.tokenize import word_tokenize
from telegram import Update
from telegram.ext import CallbackContext
nltk.download('punkt')
from helpers.telegram.typography import send_long_message
import os
import io

# Services
from services.modules.pin.pin_queries import get_all_pin
from services.modules.stats.stats_queries import get_stats, get_dashboard
from services.modules.stats.stats_capture import get_stats_capture
from services.modules.visit.visit_queries import get_all_visit, get_all_visit_csv

async def handle_ai(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()
    tokens = word_tokenize(user_message)

    res = "Sorry i dont understand your message"

    greetings = ['hello','hai']
    whos = ['who','who are you']
    self_command = ['my']
    location_command = ['marker','pin']
    stats_command = ['stats','statistic','chart','summary']
    history_command = ['history','activity','visit']

    if any(dt in tokens for dt in greetings):
        res = "Hi there! How can I assist you today?"
        await update.message.reply_text(res)
    elif any(dt in tokens for dt in whos):
        res = "Hello I'm PinMarker Bot"
        await update.message.reply_text(res)
    elif any(dt in tokens for dt in self_command):
        # Personal data
        if any(dt in tokens for dt in location_command):
            res = await get_all_pin(type='bot')
            message_chunks = send_long_message(res)
            await update.message.reply_text("Showing location...")
            for chunk in message_chunks:
                await update.message.reply_text(chunk, parse_mode='HTML')
        elif any(dt in tokens for dt in stats_command):
            res = await get_stats()
            res_capture = await get_stats_capture()
            if res_capture:
                with open(res_capture, 'rb') as photo:
                    await update.message.reply_photo(photo)
                    os.remove(res_capture)
            await update.message.reply_text(f"Showing stats...\n\n{res}", parse_mode='HTML')
        elif 'dashboard' in tokens:
            res = await get_dashboard(type='bot')
            await update.message.reply_text(f"Showing stats...\n\n{res}", parse_mode='HTML')
        elif any(dt in  tokens for dt in history_command):
            res = await get_all_visit()
            csv_content, file_name = await get_all_visit_csv(platform='telegram')
            file = io.BytesIO(csv_content.encode('utf-8'))
            file.name = file_name     
            await update.message.reply_text(f"Showing stats...\n\n{res}", parse_mode='HTML')
            await update.message.reply_document(document=file, caption="Generate CSV file of history...\n\n")
    else:
        await update.message.reply_text(res)


