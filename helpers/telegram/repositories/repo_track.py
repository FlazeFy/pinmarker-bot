import requests

# Query
async def api_get_last_track(user_id: str):
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/v1/track/last/{user_id}")
        response.raise_for_status()
        data = response.json()

        if data['data']:
            dt = data['data']
            track_lat = dt['track_lat']
            track_long = dt['track_long']
            battery_indicator = dt['battery_indicator']
            msg = f"Battery Indicator : {battery_indicator}%"

            return track_lat, track_long, msg, True
        else:
            return None, None, "No track found", False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return None, None, err_msg, False
    except KeyError:
        err_msg = "Error processing the response"
        return None, None, err_msg, False