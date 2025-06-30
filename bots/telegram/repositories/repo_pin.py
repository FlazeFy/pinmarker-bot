import requests
import csv
import io 
import httpx
# Query    
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
    
async def api_get_pin_detail_by_name(userId: str, pin_name:str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/pin/detail/name/{pin_name}/{userId}")
            response.raise_for_status()
            data = response.json()

            if data['data']:
                coor = f"{data['data']['pin_lat']},{data['data']['pin_long']}"
                res = (
                    f"<b>{data['data']['pin_name']}</b>\n\n"
                    f"Category : {data['data']['pin_category']}\n"
                    f"Latitude : {data['data']['pin_lat']}\n"
                    f"Longitude : {data['data']['pin_long']}\n"
                    f"Person In Touch : {data['data']['pin_person'] or '-'}\n"
                    f"Email : {data['data']['pin_email'] or '-'}\n"
                    f"Phone Number : {data['data']['pin_call'] or '-'}\n"
                    f"Address : {data['data']['pin_address'] or '-'}\n\n"
                    f"<b>Description</b>\n\n"
                    f"{data['data']['pin_desc'] or '<i>- No description provided -</i>'}\n\n"
                    f"https://www.google.com/maps/place/{coor}\n\n"
                    f"<b>Visit History</b>\n\n"
                )
                if data['history']:
                    for idx, dt in enumerate(data['history']):
                        res += (
                            f"{idx+1}. {dt['visit_desc']+' ' if dt['visit_desc'] else ''}using {dt['visit_by']}{' '+dt['visit_with'] if dt['visit_with'] else ''} at {dt['created_at']}\n"
                        )
                else:
                    res += '<i>- No history visit found on this pin -</i>'
                return res, data['data']['pin_lat'], data['data']['pin_long']
            else:
                return "No pin found", None, None
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, None, None
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, None, None
    
async def api_get_all_pin_export(user_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/pin_export/{user_id}")
            response.raise_for_status()
            data = response.json()

            if data['count'] > 0:
                list_file = []
                part = 1
                output = None

                for idx, dt in enumerate(data['data']):
                    if idx % 99 == 0:
                        if output is not None:
                            output.seek(0)
                            res = output.getvalue() 
                            file_bytes = io.BytesIO(res.encode('utf-8'))
                            file_bytes.name = f'Pin_List_Part-{part}.csv'
                            list_file.append(file_bytes)
                            part += 1
                        
                        output = io.StringIO()
                        writer = csv.writer(output)

                        writer.writerow([
                            "pin_name", 
                            "pin_long",
                            "pin_lat",
                        ])

                    writer.writerow([
                        dt['pin_name'], 
                        dt['pin_long'],
                        dt['pin_lat'],
                    ])

                if output is not None:
                    output.seek(0)
                    res = output.getvalue() 
                    file_bytes = io.BytesIO(res.encode('utf-8'))
                    file_bytes.name = f'Pin_List_Part-{part}.csv'
                    list_file.append(file_bytes)

                return list_file, True
            else:
                return "No pin found", False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, False

async def  api_get_nearset_pin(userId: str, max_dis:int):
    try:
        payload = {
            "user_id": userId,
            "max_distance": max_dis,
            "limit":5
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://127.0.0.1:8000/api/v1/pin/nearest/-6.2333934867861975/106.82363788271587", json=payload)
            response.raise_for_status()
            data = response.json()
            res = ''

            if data['data']:
                for idx, dt in enumerate(data['data']):
                    res += (
                        f"<b>Pin Name</b>: {dt['pin_name']}\n"
                        f"<b>Coordinate</b>: {dt['pin_coor']}\n"
                        f"<b>Distance</b>: {round(dt['distance'], 2)} m\n"
                        f"Maps : https://www.google.com/maps/place/{dt['pin_coor']}\n\n"
                    )
                return res, True
            else:
                return "No found nearest", False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, False
    
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