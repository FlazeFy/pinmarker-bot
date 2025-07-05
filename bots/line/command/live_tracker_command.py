import asyncio
# Helper
from bots.line.helper import send_location_text, send_message_text
# Repositories
from bots.repositories.repo_track import api_get_last_track

def live_tracker_command(senderId,userId):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        track_lat, track_long, msg, is_success = loop.run_until_complete(api_get_last_track(userId))
        
        if is_success:
            send_message_text(senderId, f"Showing last tracking...\n{msg}")

            if track_lat is not None and track_long is not None:
                coor = f'{track_lat}, {track_long}'
                send_location_text(senderId, 'Live Tracker Position', coor, track_lat, track_long)
        else:
            send_message_text(senderId, "Error processing the response")
    finally:
        loop.close()