from services.modules.pin.pin_queries import get_all_pin
# from helpers.discord.typography import send_long_message,convert_html_to_discord_chat
# from services.modules.stats.stats_queries import get_dashboard, get_stats
from helpers.discord.repositories.repo_pin import api_get_all_pin_export, api_get_all_pin
from helpers.discord.repositories.repo_feedback import api_get_all_feedback
from helpers.discord.repositories.repo_user import api_get_all_user

from discord import File

async def on_message_handler(bot, message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        server_name = message.guild.name if message.guild else 'Unknown Server'
        await message.channel.send(f'Hello! everyone in {server_name}. Im PinMarker Bot, what do you want me to do?')
        await message.channel.send('1. Show all pin\n2. Show all detail pin\n3. Show all dictionary\n4. Show all user\n5. Show all feedback\n6. Dashboard\n7. Stats\n')

    if message.content == '!ping':
        server_name = message.guild.name if message.guild else 'Unknown Server'
        await message.channel.send(f'Pong from {server_name}!')
    elif message.content == '1':
        res, is_success = await api_get_all_pin_export()
        if is_success:
            if len(res) == 1:
                await message.channel.send(f'Generate Exported CSV file of pin...')
            else:     
                await message.channel.send(f'Generate Exported CSV file of pin...\nSpliting into {len(res)} parts. Each of these have maximum 100 pin')
            for idx, dt in enumerate(res):
                await message.channel.send("Generate CSV file of pin...\n\n", file=File(dt, filename=f"Part-{idx+1}\n.csv"))
            await message.channel.send(f'Export finished')
        else: 
            await message.channel.send(f'{res}')
    elif message.content == '2':
        res, is_success = await api_get_all_pin()
        if is_success:
            await message.channel.send("Generate CSV file of pin...\n\n", file=File(res, filename=f"Feeback_List.csv"))
            await message.channel.send(f'Export finished')  
        else: 
            await message.channel.send(f'{res}')
    elif message.content == '4':
        res, is_success = await api_get_all_user()
        if is_success:
            await message.channel.send("Generate CSV file of user...\n\n", file=File(res, filename=f"User_List.csv"))
            await message.channel.send(f'Export finished')  
        else: 
            await message.channel.send(f'{res}')
    elif message.content == '5':
        res, is_success = await api_get_all_feedback()
        if is_success:
            await message.channel.send("Generate CSV file of feedback...\n\n", file=File(res, filename=f"Pin_List.csv"))
            await message.channel.send(f'Export finished')  
        else: 
            await message.channel.send(f'{res}')
    # elif message.content == '3':
    #     res = await get_all_visit()
    #     await send_long_message(message.channel, f"Showing history...\n\n{convert_html_to_discord_chat(res)}")
    # elif message.content == '3/csv':
    #     file, file_name = await get_all_visit_csv(platform='discord')
    #     await message.channel.send("Generate CSV file of history...\n\n", file=File(file, filename=file_name))
    # elif message.content == '4':
    #     res = await get_dashboard(type='bot')
    #     await message.channel.send(f"Showing dashboard...\n\n{convert_html_to_discord_chat(res)}")
    # elif message.content == '5':
    #     res = await get_stats()
    #     await send_long_message(message.channel, f"Showing stats...\n\n{convert_html_to_discord_chat(res)}")
    # elif message.content == '6':
    #     track_lat, track_long, msg = await get_last_tracker_position()
    #     await message.channel.send(msg)
    #     await send_long_message(message.channel, f"Showing last track position...\nhttps://www.google.com/maps/place/{track_lat},{track_long}\n\n")





