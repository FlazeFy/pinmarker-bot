import asyncio

# Helper
from bots.line.helper import send_message_text
# Repositories
from bots.repositories.repo_pin import api_get_all_pin_export

def export_pins_command(senderId, userId):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        msg, _, uploaded_link = loop.run_until_complete(api_get_all_pin_export(user_id=userId))
        
        if uploaded_link is not None:
            uploaded_link_str = ''
            for idx, dt in enumerate(uploaded_link, start=1):
                uploaded_link_str += f'Part-{idx}\n{dt}\n\n'

            send_message_text(senderId, f"Generated file (CSV) is not supported to send directly. But you can access this uploaded file from my storage.\n\n{uploaded_link_str}")
        else:
            send_message_text(senderId, msg)
    finally:
        loop.close()