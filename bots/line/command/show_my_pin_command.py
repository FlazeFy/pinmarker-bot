
import asyncio

# Repository
from bots.repositories.repo_pin import api_get_all_pin
# Helpers
from bots.line.helper import send_message_text
from bots.telegram.typography import send_long_message
from helpers.converter import strip_html_tags

def show_my_pin_command(senderId, userId):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        res, res_type, is_success, uploaded_link = loop.run_until_complete(api_get_all_pin(user_id=userId))
        
        if res_type == 'file' and is_success:
            send_message_text(senderId, f"Generated file (CSV) is not supported to send directly. But you can access this uploaded file from my storage.\n\n{uploaded_link}")
        elif res_type == 'text' and is_success:
            message_chunks = send_long_message(f"Showing Location Data:\n\n{strip_html_tags(res)}")
            for chunk in message_chunks:
                send_message_text(senderId, chunk)
        else:
            send_message_text(senderId, "Error processing the response")
    finally:
        loop.close()