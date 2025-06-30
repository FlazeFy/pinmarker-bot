import requests
import csv
import io
import httpx 

async def api_get_all_pin():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v2/pin")
            response.raise_for_status()
            data = response.json()

            if data['count'] > 0:
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
                    "Phone",
                    "Email",
                    "Is Global Shared",
                    "Created At",
                    "Created By"
                ])

                for dt in data['data']:
                    writer.writerow([
                        dt['pin_name'], 
                        dt['pin_desc'] or '-',
                        dt['pin_coordinate'],
                        dt['pin_address'] or '-',
                        dt['pin_category'],
                        dt['pin_person'] or '-',
                        dt['pin_call'] or '-',
                        dt['pin_email'] or '-',
                        dt['is_global_shared'],
                        dt['created_at'],
                        f"@{dt['created_by']}"
                    ])

                output.seek(0)
                res = output.getvalue()    

                file_bytes = io.BytesIO(res.encode('utf-8'))
                file_bytes.name = 'Pin_List.csv'

                return file_bytes, True
            else:
                return "No pin found", False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, False
    
async def api_get_all_pin_export():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v2/pin_export")
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
                            "created_at",
                            "created_by",
                        ])

                    writer.writerow([
                        dt['pin_name'], 
                        dt['pin_long'],
                        dt['pin_lat'],
                        dt['created_at'],
                        f"@{dt['created_by']}",
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