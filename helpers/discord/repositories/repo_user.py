import requests
import csv
import io 
import httpx

async def api_get_all_user():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v2/user")
            response.raise_for_status()
            data = response.json()

            if data['count'] > 0:
                output = io.StringIO()
                writer = csv.writer(output)

                # Header
                writer.writerow([
                    "ID", 
                    "Username",
                    "Email",
                    "Telegram is Valid",
                    "Telegram ID",
                    "Total Pin",
                    "Total Dictionary",
                    "Created At",
                ])

                for dt in data['data']:
                    writer.writerow([
                        dt['id'], 
                        dt['username'],
                        dt['email'],
                        f"{'True' if dt['telegram_is_valid'] else 'False'}",
                        dt['telegram_user_id'] or '-',
                        dt['total_pin'],
                        dt['total_dictionary'],
                        dt['created_at'],
                    ])

                output.seek(0)
                res = output.getvalue()    

                file_bytes = io.BytesIO(res.encode('utf-8'))
                file_bytes.name = 'User_List.csv'

                return file_bytes, True
            else:
                return "No feedback found", False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, False