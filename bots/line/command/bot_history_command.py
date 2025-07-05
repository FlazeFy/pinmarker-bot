import asyncio

# Repositories
from bots.repositories.repo_bot_history import api_get_command_history
# Helpers
from bots.line.helper import send_message_text
from bots.telegram.typography import send_long_message
from helpers.converter import strip_html_tags

def bot_history_command(senderId):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        res, res_type, is_success, uploaded_link = loop.run_until_complete(api_get_command_history(senderId))
        
        if res_type == 'file' and is_success:
            send_message_text(senderId, f"Generated file (CSV) is not supported to send directly. But you can access this uploaded file from my storage.\n\n{uploaded_link}")
        elif res_type == 'text' and is_success:
            message_chunks = send_long_message(f"Showing bot history...\n\n{strip_html_tags(res)}")
            for chunk in message_chunks:
                send_message_text(senderId, chunk)
        else:
            send_message_text(senderId, "Error processing the response")
    finally:
        loop.close()