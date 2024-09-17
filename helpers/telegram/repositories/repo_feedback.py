import requests
import httpx
# Command
async def api_post_feedback(body: str, rate:int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://127.0.0.1:8000/api/v1/feedback",
                json={
                "feedback_body": body,
                "feedback_rate": rate
            })
            response.raise_for_status()
            data = response.json()

            return data['message'], True
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, False
    except KeyError:
        err_msg = "Error processing the command"
        return err_msg, False