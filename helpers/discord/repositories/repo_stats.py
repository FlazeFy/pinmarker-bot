import requests
from services.modules.stats.stats_capture import get_stats_capture

# Query
async def api_get_summary():
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/v1/stats/dashboard/-/admin")
        response.raise_for_status()
        data = response.json()

        if data['data']:
            dt = data['data']
            res = (
                f"**Total Marker** : {dt['total_marker']}\n"
                f"**Total Favorite** : {dt['total_favorite']}\n"
                f"**Most Category** : {dt['most_category']}\n"
                f"**Last Added** : {dt['last_added']}\n"
            )
            return res, True
        else:
            return "No dashboard found", False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, False
    
async def api_capture_stats():
    try:
        stats_text = ""
        stats_img = await get_stats_capture()

        return stats_text,stats_img, True
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg,None,False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg,None,False