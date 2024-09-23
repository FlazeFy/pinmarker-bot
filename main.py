import json
from typing import Final
from telegram.ext import Application, CommandHandler,  CallbackQueryHandler, MessageHandler, filters

from configs.configs import cred
import firebase_admin
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pinmarker-36552-default-rtdb.firebaseio.com/',
    'storageBucket': 'pinmarker-36552.appspot.com'
})

# Helpers
from helpers.telegram.message_handler import start_command, button
from helpers.telegram.location_handler import location_command
from helpers.telegram.ai_handler import handle_ai

with open('configs/telegram.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN: Final = config['TOKEN']

if __name__ == '__main__':
    print('Bot is running')
    app = Application.builder().token(TOKEN).build()

    # Command
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.LOCATION, location_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai))

    print('Polling...')
    app.run_polling(poll_interval=1)
