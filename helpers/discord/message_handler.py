from services.modules.pin.pin_queries import get_all_pin
from services.modules.visit.visit_queries import get_all_visit, get_all_visit_csv
from helpers.discord.typography import send_long_message,convert_html_to_discord_chat
from services.modules.stats.stats_queries import get_dashboard, get_stats
from discord import File

async def on_message_handler(bot, message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        server_name = message.guild.name if message.guild else 'Unknown Server'
        await message.channel.send(f'Hello! everyone in {server_name}. Im PinMarker Bot, what do you want me to do?')
        await message.channel.send('1. Show my pin\n2. Show detail pin\n3. History visit\n4. Dashboard\n5. Stats\n')

    if message.content == '!ping':
        server_name = message.guild.name if message.guild else 'Unknown Server'
        await message.channel.send(f'Pong from {server_name}!')
    elif message.content == '1':
        res = await get_all_pin()
        await send_long_message(message.channel, f"Showing location...\n\n{convert_html_to_discord_chat(res)}")
    elif message.content == '3':
        res = await get_all_visit()
        await send_long_message(message.channel, f"Showing history...\n\n{convert_html_to_discord_chat(res)}")
    elif message.content == '3/csv':
        file, file_name = await get_all_visit_csv(platform='discord')
        await message.channel.send("Generate CSV file of history...\n\n", file=File(file, filename=file_name))
    elif message.content == '4':
        res = await get_dashboard()
        await message.channel.send(f"Showing dashboard...\n\n{convert_html_to_discord_chat(res)}")
    elif message.content == '5':
        res = await get_stats()
        await send_long_message(message.channel, f"Showing stats...\n\n{convert_html_to_discord_chat(res)}")





