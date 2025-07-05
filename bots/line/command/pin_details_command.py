
import asyncio

# Repositories
from bots.repositories.repo_pin import api_get_all_pin_name
# Helpers
from bots.telegram.typography import send_long_message
from helpers.converter import strip_html_tags
from bots.line.helper import send_message_text

def pin_details_command(senderId, userId):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        res = loop.run_until_complete(api_get_all_pin_name(userId))
        
        message_chunks = send_long_message(strip_html_tags(res))
        for chunk in message_chunks:
            send_message_text(senderId, chunk)
    finally:
        loop.close()