import requests
import httpx
from firebase_admin import storage
from datetime import datetime
import csv
import io 

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
    
async def api_get_all_pin(user_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/pin/{user_id}")
            response.raise_for_status()
            data = response.json()

            if data['count'] > 0:
                if data['count'] > 30:
                    output = io.StringIO()
                    writer = csv.writer(output)

                    # Header
                    writer.writerow([
                        "Name", 
                        "Description",
                        "Coordinate",
                        "Address",
                        "Category",
                        "Person in Touch",
                        "Total Visit",
                        "Last Visit",
                        "Created At"
                    ])

                    for dt in data['data']:
                        writer.writerow([
                            dt['pin_name'], 
                            dt['pin_desc'] or '-',
                            dt['pin_coordinate'],
                            dt['pin_address'] or '-',
                            dt['pin_category'],
                            dt['pin_person'] or '-',
                            dt['total_visit'],
                            dt['last_visit'] or '-',
                            dt['created_at']
                        ])

                    output.seek(0)
                    res = output.getvalue()    

                    # Firebase Storage
                    bucket = storage.bucket()
                    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    fileName = f"pin_list_{user_id}_{now_str}.csv"
                    blob = bucket.blob(f"generated_data/pin/{fileName}")
                    blob.upload_from_string(res, content_type="text/csv")
                    blob.make_public()
                    download_url = blob.public_url

                    file_bytes = io.BytesIO(res.encode('utf-8'))
                    file_bytes.name = 'Pin_List.csv'

                    return file_bytes, 'file', True, download_url
                else:
                    res = ''
                    for item in data['data']:
                        res += (
                            f"<b>{item['pin_name']}</b> - {item['pin_category']}\n"
                            f"{item['pin_desc']or '-'}\n"
                            f"https://www.google.com/maps/place/{item['pin_coordinate']}\n\n"
                            f"Person in Touch : {item['pin_person'] or '-'}\n"
                            f"Address : {item['pin_address'] or '-'}\n"
                            f"Total / Last Visit : {item['total_visit']} / {item['last_visit']or '-'}\n"
                            f"Created At : {item['created_at'] or '-'}\n\n"
                            f"========== || ========== || ==========\n\n"
                        )
                    return res, 'text', True, None
            else:
                return "No pin found", "text", False, None
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, "text", False, None
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, "text", False, None
       
async def api_get_all_pin_name(userId: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/pin/{userId}")
            response.raise_for_status()
            data = response.json()

            if data['data']:
                res = f"Showing all pin. Type detail/*Pin Name* to see the detail\nfor example type <b>detail {data['data'][0]['pin_name']}</b>\n\n"
                for idx, dt in enumerate(data['data']):
                    res += (
                        f"{idx+1}. {dt['pin_name']}\n"
                    )
                return res
            else:
                return "No pin found"
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg