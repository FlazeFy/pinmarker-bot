import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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