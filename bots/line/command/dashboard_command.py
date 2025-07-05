import asyncio

# Helper
from bots.line.helper import send_message_text
# Repositories
from bots.repositories.repo_stats import api_get_dashboard

def dashboard_command(senderId, userId):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        res, is_success = loop.run_until_complete(api_get_dashboard(user_id=userId))
        
        if is_success is not None:
            send_message_text(senderId, f"Showing dashboard...\n{res}\n")
        else:
            send_message_text(senderId, res)
    finally:
        loop.close()