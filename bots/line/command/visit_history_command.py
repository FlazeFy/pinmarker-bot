import asyncio

# Helper
from bots.line.helper import send_message_text
from bots.repositories.repo_visit import api_get_visit_history
from bots.telegram.typography import send_long_message
from helpers.converter import strip_html_tags

def visit_history_command(senderId, userId, message_text):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        res, type, uploaded_link = loop.run_until_complete(api_get_visit_history(userId, '30' if message_text == '/visit_last_30d' else 'all'))
        
        if type == 'file':
            uploaded_link_str = ''
            for idx, dt in enumerate(uploaded_link, start=1):
                uploaded_link_str += f'Part-{idx}\n{dt}\n\n'

            send_message_text(senderId, f"Generated file (CSV) is not supported to send directly. But you can access this uploaded file from my storage.\n\n{uploaded_link_str}")
        elif type == 'text':
            message_chunks = send_long_message(strip_html_tags(res))
            for chunk in message_chunks:
                send_message_text(senderId, chunk)
        else:
            send_message_text(senderId, "Error processing the response")
    finally:
        loop.close()