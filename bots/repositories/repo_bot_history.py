import requests
import csv
import httpx
import io
# Helper
from helpers.file_handling.upload import upload_firebase_storage 

# Query
async def api_get_command_history(socmed_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/bot_history/{socmed_id}")
            response.raise_for_status()
            data = response.json()

            if data['count'] > 0:
                if data['count'] < 30:
                    output = io.StringIO()
                    writer = csv.writer(output)

                    # Header
                    writer.writerow([
                        "Command", 
                        "Created At",
                        "Total"
                    ])

                    for dt in data['data']:
                        writer.writerow([
                            dt['command'], 
                            dt['created_at'],
                            dt['total'],
                        ])

                    output.seek(0)
                    res = output.getvalue()    
                    download_url = upload_firebase_storage(socmed_id, 'bot_history', 'csv', res)

                    file_bytes = io.BytesIO(res.encode('utf-8'))
                    file_bytes.name = 'Bot_History.csv'

                    return file_bytes, 'file', True, download_url
                elif data['count'] > 0:
                    res = "\n".join([f"Command: {item['command']}\nCreated At: {item['created_at']}" for item in data['data']])
                    return res, 'text', True, None
            else:
                return "No history found", "text", False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, "text", False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, "text", False