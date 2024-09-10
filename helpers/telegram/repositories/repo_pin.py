import requests
import csv
import io 
from firebase_admin import storage
from datetime import datetime

# Query
async def api_get_all_pin(user_id: str, max_dis: str):
    try:
        payload = {
            "id": user_id,
            "max_distance": max_dis
        }
        response = requests.get(f"http://127.0.0.1:8000/api/v1/pin/nearest/-6.2333934867861975/106.82363788271587",json=payload)
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

                file_bytes = io.BytesIO(res.encode('utf-8'))
                file_bytes.name = 'Pin_List.csv'

                return file_bytes, 'file', True
            elif data['count'] > 0:
                res = "\n".join([f"Name: {item['pin_name']}\nDescription: {item['pin_desc']or '-'}\nCoordinate: {item['pin_coordinate']}\nAddress: {item['pin_address']or '-'}\nCategory: {item['pin_category']}\nPerson in Touch: {item['pin_person']or '-'}\nCreated At: {item['created_at']or '-'}\n" for item in data['data']])
                return res, 'text', True
        else:
            return "No pin found", False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, False
    
async def api_get_all_pin_export(user_id: str):
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/v1/pin_export/{user_id}")
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
            "id": userId,
            "max_distance": max_dis
        }
        response = requests.post(f"http://127.0.0.1:8000/api/v1/pin/nearest/-6.2333934867861975/106.82363788271587", json=payload)
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