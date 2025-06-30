import discord
from typing import Final
import json
import os

from configs.configs import cred
import firebase_admin
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pinmarker-36552-default-rtdb.firebaseio.com/',
    'storageBucket': 'pinmarker-36552.appspot.com'
})

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# Helpers
from bots.discord.message_handler import on_message_handler
from bots.discord.ready_handler import on_ready_handler

with open('configs/discord.json', 'r') as config_file:
    config = json.load(config_file)
TOKEN: Final = config['TOKEN']

@bot.event
async def on_ready():
    await on_ready_handler(bot)

@bot.event
async def on_message(message):
    await on_message_handler(bot, message)

bot.run(TOKEN)
