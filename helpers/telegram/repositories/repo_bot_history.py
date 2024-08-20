import requests
import csv
import io 

# Query
async def api_get_command_history(tele_id: str):
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/v1/bot_history/{tele_id}")
        response.raise_for_status()
        data = response.json()

        if data['count'] > 0:
            if data['count'] > 0:
                output = io.StringIO()
                writer = csv.writer(output)

                # Header
                writer.writerow([
                    "Command", 
                    "Created At"
                ])

                for dt in data['data']:
                    writer.writerow([
                        dt['command'], 
                        dt['created_at'],
                    ])

                output.seek(0)
                res = output.getvalue()    

                file_bytes = io.BytesIO(res.encode('utf-8'))
                file_bytes.name = 'Bot_History.csv'

                return file_bytes, 'file', True
            elif data['count'] > 0:
                res = "\n".join([f"Command: {item['command']}\nCreated At: {item['created_at']}" for item in data['data']])
                return res, 'text', True
        else:
            return "No history found.", False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, None, False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, None, False