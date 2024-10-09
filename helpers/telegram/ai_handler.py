import nltk
from nltk.tokenize import word_tokenize
from telegram import Update
from telegram.ext import CallbackContext
nltk.download('punkt')
import os
import re
import random

# Helper
from helpers.telegram.typography import send_long_message
from helpers.generator import get_city_from_coordinate
from helpers.sqlite.template import post_ai_command
from helpers.telegram.repositories.repo_user import api_get_profile_by_telegram_id
from helpers.telegram.repositories.repo_stats import api_get_dashboard
from helpers.telegram.repositories.repo_visit import api_get_visit_history
from helpers.telegram.repositories.repo_pin import api_get_pin_detail_by_name, api_get_all_pin_name

# Services
from services.modules.pin.pin_queries import get_all_pin, get_find_all, get_pin_by_category_query, get_pin_by_name
from services.modules.stats.stats_queries import get_stats, get_dashboard
from services.modules.stats.stats_capture import get_stats_capture

async def handle_ai(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()
    tokens = word_tokenize(user_message)
    userTeleId = update.effective_user.id
    profile = await api_get_profile_by_telegram_id(teleId=userTeleId)

    res = "Sorry i dont understand your message"

    # Receive order
    greetings = ['hello','hai']
    whos = ['who','who are you']
    thanks = ['thank','thanks','thx','thank you','thanks a lot']
    self_command = ['my']
    location_command = ['marker','pin']
    stats_command = ['stats','statistic','chart','summary']
    visit_command = ['visit']
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
    userId = profile['data']['id']

    if any(dt in tokens for dt in greetings):
        res = "Hi there! How can I assist you today?"
        await update.message.reply_text(res)
    elif any(dt in tokens for dt in whos):
        res = "Hello I'm PinMarker Bot"
        await update.message.reply_text(res)
    elif any(dt in tokens for dt in thanks):
        res = ['Your welcome','At my pleasure']
        await update.message.reply_text(random.choice(res))
    elif any(dt in tokens for dt in ['detail']):
        search = ' '.join(tokens).replace("detail","").strip()

        if search == "":
            res = await api_get_all_pin_name(userId=userId)
            message_chunks = send_long_message(res)
            for chunk in message_chunks:
                await update.message.reply_text(f"Can you specify more detail of the pin by this name...\n\n{chunk}", parse_mode='HTML')
        else:
            res, lat, long = await api_get_pin_detail_by_name(userId=userId,pin_name=search)
            message_chunks = send_long_message(res)
            for chunk in message_chunks:
                await update.message.reply_text(f"{random.choice(present_respond)} pin detail...\n\n{chunk}", parse_mode='HTML')
            if lat and long:
                await update.message.reply_location(latitude=lat, longitude=long)
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
            elif any(dt in tokens for dt in visit_command):
                def extract_days_from_tokens(tokens):
                    text = ' '.join(tokens)
                    match = re.search(r'(\d+)\s+day(s)?', text, re.IGNORECASE)
                    if match:
                        return str(match.group(1))
                    else:
                        return 'all'
                    
                search_tokens = [token for token in tokens if token not in visit_command + self_command]
                days = extract_days_from_tokens(tokens)
                res, type = await api_get_visit_history(user_id=userId, days=days)
                if type == 'file':
                    if len(res) == 1:
                        await update.message.reply_text("Generate Exported CSV file of visit history...")     
                    else:     
                        await update.message.reply_text("Generate Exported CSV file of visit history...\nSpliting into {len(res)} parts. Each of these have maximum 100 history")     
                    for idx, dt in enumerate(res):
                        await update.message.reply_document(document=dt, caption=f"Part-{idx+1}\n")
                    await update.message.reply_text("Export finished")
                elif type == 'text':
                    message_chunks = send_long_message(res)
                    for chunk in message_chunks:
                        await update.message.reply_text(chunk,parse_mode='HTML')
                else:
                    await update.message.reply_text("Error processing the response",parse_mode='HTML') 
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


