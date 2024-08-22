import nltk
from nltk.tokenize import word_tokenize
from telegram import Update
from telegram.ext import CallbackContext
nltk.download('punkt')

# Helper
from helpers.telegram.typography import send_long_message
from helpers.generator import get_city_from_coordinate
from helpers.sqlite.template import post_ai_command

from helpers.telegram.repositories.repo_stats import api_get_dashboard

import os
import io
import random

# Services
from services.modules.pin.pin_queries import get_all_pin, get_find_all, get_pin_by_category_query, get_pin_by_name
from services.modules.stats.stats_queries import get_stats, get_dashboard
from services.modules.stats.stats_capture import get_stats_capture
from services.modules.visit.visit_queries import get_all_visit_last_day, get_all_visit_csv
from services.modules.user.user_queries import get_profile_by_telegram_id

async def handle_ai(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()
    tokens = word_tokenize(user_message)
    userTeleId = update.effective_user.id
    profile = await get_profile_by_telegram_id(teleId=userTeleId)

    res = "Sorry i dont understand your message"

    # Receive order
    greetings = ['hello','hai']
    whos = ['who','who are you']
    thanks = ['thank','thanks','thx','thank you','thanks a lot']
    self_command = ['my']
    location_command = ['marker','pin']
    stats_command = ['stats','statistic','chart','summary']
    history_command = ['history','activity','visit']
    where_command = ['where','locate','find','search']
    where_command_region = ['city','town','village','region']
    topic_self_command = ["i'm","im"]

    # Topic order
    topic_food_command = ['hungry','thirsty','starved']
    topic_social_command = ['lonely','sad','bored']
    topic_personal_command = ['tired','sick']

    # Respond / Presenting data
    present_respond = ['Showing','Let me show you the',"Here's the","I got the","See this"]

    post_ai_command(socmed_id=userTeleId, socmed_platform='telegram', command=user_message)

    role = profile['role']
    userId = profile['data'].id

    if any(dt in tokens for dt in greetings):
        res = "Hi there! How can I assist you today?"
        await update.message.reply_text(res)
    elif any(dt in tokens for dt in whos):
        res = "Hello I'm PinMarker Bot"
        await update.message.reply_text(res)
    elif any(dt in tokens for dt in thanks):
        res = ['Your welcome','At my pleasure']
        await update.message.reply_text(random.choice(res))
    elif any(dt in tokens for dt in self_command):
        if profile["is_found"]:
            # Personal data
            if any(dt in tokens for dt in location_command):
                res = await get_all_pin(type='bot', userId=userId)
                message_chunks = send_long_message(res)
                await update.message.reply_text(f"{random.choice(present_respond)} location...")
                for chunk in message_chunks:
                    await update.message.reply_text(chunk, parse_mode='HTML')
            elif any(dt in tokens for dt in stats_command):
                res = await get_stats(userId=userId)
                res_capture = await get_stats_capture()
                if res_capture:
                    with open(res_capture, 'rb') as photo:
                        await update.message.reply_photo(photo)
                        os.remove(res_capture)
                await update.message.reply_text(f"{random.choice(present_respond)} stats...\n\n{res}", parse_mode='HTML')
            elif 'dashboard' in tokens:
                res, is_success = await api_get_dashboard(tele_id=userId, role=role)
                if is_success:
                    await update.message.reply_text(f"{random.choice(present_respond)} dashboard...\n\n{res}", parse_mode='HTML')
                else:
                    await update.message.reply_text(f"{random.choice(present_respond)} dashboard...\n\n{res}", parse_mode='HTML')
            
            # Visit history
            elif any(dt in  tokens for dt in history_command):
                res = await get_all_visit_last_day(userId=userId, teleId=userTeleId)
                csv_content, file_name = await get_all_visit_csv(platform='telegram',userId=userId,teleId=userTeleId)
                if csv_content and file_name:
                    file = io.BytesIO(csv_content.encode('utf-8'))
                    file.name = file_name     
                    await update.message.reply_text(f"{random.choice(present_respond)} stats...\n\n{res}", parse_mode='HTML')
                    await update.message.reply_document(document=file, caption="Generate CSV file of history...\n\n")
                else:
                    await update.message.reply_text(f"Export failed, {file_name}", parse_mode='HTML')
        else:
            await update.message.reply_text("You're not signed in yet")

    # Topic data
    elif any(dt in tokens for dt in topic_self_command):
        res =''
        topic_respond = ['Here some list where you can solve your problem']

        # Cafe, Restaurant
        if any(dt in tokens for dt in topic_food_command):
            data = await get_pin_by_category_query(category="cafe,restaurant",user_id=userId)
            topic_respond.extend(['You can enjoy some food or drink at','Try to get food at'])
            if data['data']:
                for idx, dt in enumerate(data['data'], 1):
                    res += (
                        f"<b>{idx}. {dt['pin_name']}</b>\n"
                        f"https://www.google.com/maps/place/{dt['pin_lat']},{dt['pin_long']}\n\n"
                    )
            else:
                res += 'No data found'
            await update.message.reply_text(f"{random.choice(topic_respond)}:\n\n{res}", parse_mode='HTML')

        # Family, Friend
        elif any(dt in tokens for dt in topic_social_command):
            data = await get_pin_by_category_query(category="family,friend",user_id=userId)
            topic_respond.extend(['I think you need to talk to these people','Remember you are not alone','Go have fun with'])
            if data['data']:
                for idx, dt in enumerate(data['data'], 1):
                    res += (
                        f"<b>{idx}. {dt['pin_name']}</b>\n"
                        f"https://www.google.com/maps/place/{dt['pin_lat']},{dt['pin_long']}\n\n"
                    )
            else:
                res += 'No data found'
            await update.message.reply_text(f"{random.choice(topic_respond)}:\n\n{res}", parse_mode='HTML')

        # Personal
        elif any(dt in tokens for dt in topic_personal_command):
            data = await get_pin_by_category_query(category="personal",user_id=userId)
            topic_respond.extend(['You need your bed right now'])
            if data['data']:
                for idx, dt in enumerate(data['data'], 1):
                    res += (
                        f"<b>{idx}. {dt['pin_name']}</b>\n"
                        f"https://www.google.com/maps/place/{dt['pin_lat']},{dt['pin_long']}\n\n"
                    )
            else:
                res += 'No data found'
            await update.message.reply_text(f"{random.choice(topic_respond)}:\n\n{res}", parse_mode='HTML')

    # Find marker
    elif any(dt in tokens for dt in where_command):
        search_tokens = [token for token in tokens if token not in where_command + where_command_region]
        search = ' '.join(search_tokens)
        if any(dt in tokens for dt in where_command_region):
            data = await get_pin_by_name(name=search)
            res = ''
            if data['data']:
                res = f"{random.choice(present_respond)} marker...\n\n"
                for idx, dt in enumerate(data['data'], 1):
                    res += (
                        f"<b>{idx}. {dt['pin_name']} at {get_city_from_coordinate(dt['pin_lat'],dt['pin_long'])}</b>\n"
                        f"https://www.google.com/maps/place/{dt['pin_lat']},{dt['pin_long']}\n\n"
                    )
            else:
                res += 'No data found'
        else:
            res = await get_find_all(search=search, type='ai')

        message_chunks = send_long_message(res)
        for chunk in message_chunks:
            await update.message.reply_text(chunk, parse_mode='HTML')
            
    else:
        await update.message.reply_text(res)


