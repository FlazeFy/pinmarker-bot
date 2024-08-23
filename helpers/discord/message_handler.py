import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

from helpers.discord.repositories.repo_pin import api_get_all_pin_export, api_get_all_pin
from helpers.discord.repositories.repo_feedback import api_get_all_feedback
from helpers.discord.repositories.repo_user import api_get_all_user

from discord import File

async def on_message_handler(bot, message):
    user_message = message.content.lower()
    tokens = word_tokenize(user_message)

    res = "Sorry i dont understand your message"

    # Receive order
    greetings = ['hello','hai']
    whos = ['who','who are you']
    thanks = ['thank','thanks','thx','thank you','thanks a lot']
    global_command = ['list','global','pin']
    pin_command = ['pin','marker']
    feedback_command = ['feedback']
    user_command = ['user']
    where_command = ['where','locate','find','search']
    generate_command = ['generate','print','csv','export']

    # Respond / Presenting data
    present_respond = ['Showing','Let me show you the',"Here's the","I got the","See this"]

    # Usecase
    async def usecase_get_all_pin():
        res, is_success = await api_get_all_pin()
        if is_success:
            await message.channel.send("Generate CSV file of pin...\n\n", file=File(res, filename=f"Feeback_List.csv"))
            await message.channel.send(f'Export finished')  
        else: 
            await message.channel.send(f'{res}')
    async def usecase_get_all_pin_export():
        res, is_success = await api_get_all_pin_export()
        if is_success:
            if len(res) == 1:
                await message.channel.send(f'Generate Exported CSV file of pin...')
            else:     
                await message.channel.send(f'Spliting into {len(res)} parts. Each of these have maximum 100 pin')
            for idx, dt in enumerate(res):
                await message.channel.send("Generate CSV file of pin...\n\n", file=File(dt, filename=f"Part-{idx+1}\n.csv"))
            await message.channel.send(f'Export finished')
        else: 
            await message.channel.send(f'{res}')
    async def usecase_get_all_feedback():
        res, is_success = await api_get_all_feedback()
        if is_success:
            await message.channel.send("Generate CSV file of feedback...\n\n", file=File(res, filename=f"Pin_List.csv"))
            await message.channel.send(f'Export finished')  
        else: 
            await message.channel.send(f'{res}')

    async def usecase_get_all_user():
        res, is_success = await api_get_all_user()
        if is_success:
            await message.channel.send("Generate CSV file of user...\n\n", file=File(res, filename=f"User_List.csv"))
            await message.channel.send(f'Export finished')  
        else: 
            await message.channel.send(f'{res}')

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        server_name = message.guild.name if message.guild else 'Unknown Server'
        await message.channel.send(f'Hello! everyone in {server_name}. Im PinMarker Bot, what do you want me to do?')
        await message.channel.send('1. Show all pin\n2. Show all detail pin\n3. Show all dictionary\n4. Show all user\n5. Show all feedback\n6. Dashboard\n7. Stats\n\nOr you can type what you want and we will search for it')

    # NLP Bot
    if any(dt in tokens for dt in greetings):
        res = "Hi there! How can I assist you today?"
        await message.channel.send(res)
    elif any(dt in tokens for dt in whos):
        res = "Hello I'm PinMarker Bot"
        await message.channel.send(res)
    elif any(dt in tokens for dt in thanks):
        res = ['Your welcome','At my pleasure']
        await message.channel.send(res)
    elif any(dt in tokens for dt in generate_command):
        if any(dt in tokens for dt in pin_command):
            if any(dt in tokens for dt in ['header','short','import','split']):
                await usecase_get_all_pin_export()
            else:
                await usecase_get_all_pin()

        elif any(dt in tokens for dt in feedback_command): 
            await usecase_get_all_feedback()

        elif any(dt in tokens for dt in user_command): 
            await usecase_get_all_user()
    else:
        if message.content == '!ping':
            server_name = message.guild.name if message.guild else 'Unknown Server'
            await message.channel.send(f'Pong from {server_name}!')
        elif message.content == '1':
            await usecase_get_all_pin_export()

        elif message.content == '2':
            await usecase_get_all_pin()

        elif message.content == '4':
            await usecase_get_all_user()

        elif message.content == '5':
            await usecase_get_all_feedback()
            





