import requests
import httpx

# Query
async def api_get_profile_by_telegram_id(teleId: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/user/check/{teleId}")
            response.raise_for_status()
            data = response.json()
            return data
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg