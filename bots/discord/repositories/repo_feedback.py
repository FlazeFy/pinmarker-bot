import requests
import csv
import io 
import httpx

async def api_get_all_feedback():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/feedback")
            response.raise_for_status()
            data = response.json()

            if data['count'] > 0:
                output = io.StringIO()
                writer = csv.writer(output)

                # Header
                writer.writerow([
                    "Feedback", 
                    "Rate",
                    "Created By"
                ])

                for dt in data['data']:
                    writer.writerow([
                        dt['feedback_body'], 
                        dt['feedback_rate'],
                        dt['created_at'],
                    ])

                output.seek(0)
                res = output.getvalue()    

                file_bytes = io.BytesIO(res.encode('utf-8'))
                file_bytes.name = 'Pin_List.csv'

                return file_bytes, True
            else:
                return "No feedback found", False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, False