import json
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler,  CallbackQueryHandler

from configs.configs import cred
import firebase_admin
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pinmarker-36552-default-rtdb.firebaseio.com/',
    'storageBucket': 'pinmarker-36552.appspot.com'
})

# Helpers
from helpers.greeting import start_command, button

with open('configs/telegram.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN: Final = config['TOKEN']

if __name__ == '__main__':
    print('Bot is running')
    app = Application.builder().token(TOKEN).build()

    # Command
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(button))

    print('Polling...')
    app.run_polling(poll_interval=10)
