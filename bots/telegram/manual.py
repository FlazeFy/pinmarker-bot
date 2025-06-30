import json
from typing import Final
from telegram import Bot
from telegram.constants import ParseMode

with open('configs/telegram.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN: Final = config['TOKEN']

async def send_tele_chat(tele_id: str, msg: str, file_path: str = None):
    bot = Bot(token=TOKEN)

    if file_path:
        await bot.send_document(
            chat_id=tele_id,
            document=file_path,
            caption=msg,
            parse_mode=ParseMode.HTML
        )
    else:
        await bot.send_message(
            chat_id=tele_id,
            text=msg,
            parse_mode='HTML'
        )