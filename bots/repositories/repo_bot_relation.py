import httpx

# Command
async def api_post_check_bot_relation(context_id: str, source_type: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://127.0.0.1:8000/api/v1/bot_relation/check",
                json={
                    "context_id": context_id,
                    "relation_type": source_type,
                    "relation_platform": "line"
                }
            )
            response.raise_for_status()
            data = response.json()

            return True, None, data['data']

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return False, None, None
        else:
            return False, e, None

    except httpx.RequestError as e:
        return False, e, None

    except Exception as e:
        return False, e, None
    
async def api_post_create_bot_relation(context_id: str, relation_name: str,source_type: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://127.0.0.1:8000/api/v1/bot_relation/create",
                json={
                    "context_id":context_id,
                    "relation_type":source_type,
                    "relation_platform":"line",
                    "relation_name":relation_name
                }
            )
            if response.status_code == 201:
                return True, None
            return False, None

    except httpx.HTTPStatusError as e:
        return False, f"HTTP error: {e.response.status_code}"

    except httpx.RequestError as e:
        return False, f"Request error: {str(e)}"

    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
