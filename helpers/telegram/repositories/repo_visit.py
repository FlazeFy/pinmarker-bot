import requests
import csv
import io 
import httpx

async def api_get_visit_history(user_id: str, days:str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/api/v1/visit/history/{user_id}/{days}")
            response.raise_for_status()
            data = response.json()

            if data['count'] > 0:
                if data['count'] > 30:
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

                            datetimeCol = "Visit At"
                            if data['with_timezone']:
                                datetimeCol = f"Visit At UTC({data['with_timezone']})"

                            writer.writerow([
                                "Pin Name",
                                "Pin Category",
                                "Coordinate", 
                                "Description",
                                "Visit By",
                                "Companion",
                                datetimeCol
                            ])

                        writer.writerow([
                            dt['pin_name'] or '-',
                            dt['pin_category'],
                            dt['pin_coordinate'] or '-', 
                            dt['visit_desc'] or '-',
                            dt['visit_by'],
                            dt['visit_with'] or '-',
                            dt['created_at']
                        ])

                    if output is not None:
                        output.seek(0)
                        res = output.getvalue() 
                        file_bytes = io.BytesIO(res.encode('utf-8'))
                        file_bytes.name = f'Visit_List_Part-{part}.csv'
                        list_file.append(file_bytes)

                    return list_file, 'file'
                else:
                    if days != 'all':
                        res = f'Showing visit history in past {days} days :\n\n'
                    else:
                        res = f'Showing all visit history :\n\n'
                    for dt in data['data']:
                        visitWith = ""
                        if dt['visit_with'] != "":
                            visitWith = f" with {dt['visit_with']}"
                        res += (
                            f"- Visit at {dt['pin_name'] if dt['pin_name'] else dt['visit_desc']} using {dt['visit_by']}{visitWith} at {dt['created_at']}\n\n"
                        )
                    return res, 'text'
            else:
                return "No visit history found", 'text'
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"No visit history found for {'last ' if days != 'all' else ''}{days} days", 'text'
        else:
            err_msg = f"Something went wrong: {e}"
            return err_msg, 'text'
    except requests.exceptions.RequestException as e:
        err_msg = f"Something went wrong: {e}"
        return err_msg, 'text'
    except KeyError:
        err_msg = "Error processing the response"
        return err_msg, 'text'