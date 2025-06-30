import requests
import httpx
    
async def api_get_nearset_pin_share_loc(userId: str, max_dis:int, lat:float, long:float):
    try:
        payload = {
            "user_id": userId,
            "max_distance": max_dis,
            "limit":10
        }
        async with httpx.AsyncClient() as client:
            if userId:
                response = await client.post(f"http://127.0.0.1:8000/api/v1/pin/nearest/{lat}/{long}", json=payload)
            else: 
                response = await client.post(f"http://127.0.0.1:8000/api/v1/pin_global/nearest/{lat}/{long}", json=payload)
            response.raise_for_status()
            data = response.json()
            res = ''

            if data['data']:
                for dt in data['data']:
                    distance = dt['distance']
                    if distance > 1000:
                        distance = distance / 1000
                        distance = f"{distance:.2f} km"
                    else:
                        distance = f"{distance:.2f} m"

                    if userId:
                        res += (
                            f"<b>{dt['pin_category']} - {dt['pin_name']}</b>\n"
                            f"Distance from Me: <b>{distance}</b>\n\n"
                            f"<b>Description</b>\n"
                            f"{dt['pin_desc'] or '<i>- No description provided -</i>'}\n"
                            f"<b>Contact</b>\n"
                            f"Person in Touch : {dt['pin_person'] or '-'}\n"
                            f"Phone Number : {dt['pin_call'] or '-'}\n"
                            f"Email : {dt['pin_email'] or '-'}\n"
                            f"Address : {dt['pin_address'] or '-'}\n"
                            f"https://www.google.com/maps/place/{dt['pin_coor']}\n\n"
                            f"========== || ========== || ==========\n\n"
                        )
                    else:
                        res += (
                            f"<b>{dt['pin_category']} - {dt['pin_name']}</b>\n"
                            f"Distance from Me: <b>{distance}</b>\n\n"
                            f"<b>Description</b>\n"
                            f"{dt['pin_desc'] or '<i>- No description provided -</i>'}\n"
                            f"Address : {dt['pin_address'] or '-'}\n"
                            f"https://www.google.com/maps/place/{dt['pin_coor']}\n\n"
                            f"========== || ========== || ==========\n\n"
                        )
                return res
            else:
                return "No found nearest"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return "No found nearest"
        else:
            return "Something went wrong"
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg