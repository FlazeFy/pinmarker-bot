import json
from typing import Final
from telegram import Bot

with open('configs/telegram.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN: Final = config['TOKEN']

async def send_tele_chat(tele_id:str,msg:str):
    bot = Bot(token=TOKEN)
    await bot.send_message(
        chat_id=tele_id,
        text=msg,
        parse_mode='HTML'
    )