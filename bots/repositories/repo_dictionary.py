import requests
import httpx

# Query
async def api_get_dictionary_by_type(dictionary_type, user_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/dct/{dictionary_type}/{user_id}")
            response.raise_for_status()
            data = response.json()

            return data['message'], data['data']
    except requests.exceptions.RequestException as e:
        return e, None
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, None