import requests
import httpx 

async def api_get_global_list(search:str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/pin_global/{search}")
            response.raise_for_status()
            data = response.json()

            if data['count'] > 0:
                data = data['data']
                msg = ''
                for idx, dt in enumerate(data):
                    tags = ''
                    if dt['list_tag']:
                        num_tags = len(dt['list_tag'])
                        for idx_tag, tag in enumerate(dt['list_tag']):
                            if num_tags == 1:
                                tags = f"#{tag['tag_name']}"
                            elif idx_tag < num_tags - 1:
                                tags += f"#{tag['tag_name']}, "
                            else:
                                tags += f"and #{tag['tag_name']}"
                    msg += (
                        f"**{idx}. {dt['list_name']}**"
                        f"{dt['list_desc']} {tags}\n"
                        f"**List Marker ({dt['total']})**\n"
                        f"{dt['pin_list']}\n"
                        f"**Created At**\n"
                        f"{dt['created_at']} by @{dt['created_by']}\n"
                        f"*See on web version https://pinmarker.leonardhors.com/LoginController/view/{search.replace(' ','_')}*\n\n"
                    )
                return msg, 'text', False
            else:
                return "No global list found", 'text', False
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, None, False
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, None, False