import requests
import httpx
# Query
async def api_get_dashboard(tele_id: str, role:str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/stats/dashboard/{tele_id}/{role}")
            response.raise_for_status()
            data = response.json()

            if data['data']:
                dt = data['data']
                res = (
                    f"<b>Total Marker: {dt['total_marker']}</b>\n"
                    f"<b>Total Favorite : {dt['total_favorite']}</b>\n"
                    f"<b>Most Category : {dt['most_category']}</b>\n"
                    f"<b>Last Added : {dt['last_added']}</b>\n"
                )
                if role == 'user':
                    res += (
                        f"<b>Last Visit : {dt['last_visit']}</b>\n"
                        f"<b>Most Visit : {dt['most_visit']}</b>\n"
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