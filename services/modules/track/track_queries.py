import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta

async def get_last_tracker_position():
    userId = 'fcd3f23e-e5aa-11ee-892a-3216422910e9'
    ref = db.reference('track_live_'+userId)
    query = ref.order_by_child('created_at').limit_to_last(1)
    data = query.get()

    if data:
        data_values = list(data.values())
        if data_values:
            track_lat = data_values[0]['track_lat']
            track_long = data_values[0]['track_long']
            battery_indicator = data_values[0]['battery_indicator']
            msg = f"Battery Indicator : {battery_indicator}%"

            return track_lat, track_long, msg
    return None

async def get_tracks(userId:str):
    ref = db.reference('track_live_'+userId)
    query = ref.order_by_child('created_at').limit_to_last(10)
    data = query.get()

    if data:
        data_values = list(data.values())
        return {
            "data": data_values,
            "message": "Track journey found",
            "count": len(data_values)
        }
    else:
        return {
            "message": "No Track journey found",
        }
    
async def get_tracks_period(userId: str, start_time: datetime = None, end_time: datetime = None):
    ref = db.reference('track_live_' + userId)
    
    query = ref.order_by_child('created_at')
    
    if start_time:
        start_time_str = start_time.isoformat(timespec='microseconds')
        query = query.start_at(start_time_str)
    
    if end_time:
        end_time_str = end_time.isoformat(timespec='microseconds')
        query = query.end_at(end_time_str)
    
    data = query.get()
    
    if data:
        data_values = list(data.values())
        return {
            "data": data_values,
            "message": "Track journey found",
            "count": len(data_values)
        }
    else:
        return {
            "message": "No Track journey found",
        }