import csv
import io
import httpx

from helpers.telegram.manual import send_tele_chat
from services.modules.user.admin_queries import get_all_admin_contact

async def audit_show_all_feedback_every_week():
    async with httpx.AsyncClient() as client:
        # Fetch Admin Contact
        admins = await get_all_admin_contact()

        # Fetch Feedback
        res = await client.get("http://localhost:8000/api/v1/feedback") 
        res.raise_for_status()
        data = res.json()

        if data["count"] == 0 or not data["data"]:
            if admins:
                for idx, dt in enumerate(admins):
                    await send_tele_chat(tele_id=dt.telegram_user_id,msg=f"[ADMIN] Hello {dt.username}, I just checked the feedback, and not found anything")
        else:
            list_file = []
            part = 1
            output = None

            for idx, dt in enumerate(data['data']):
                # Generate CSV
                if idx % 99 == 0:
                    if output is not None:
                        output.seek(0)
                        res = output.getvalue() 
                        file_bytes = io.BytesIO(res.encode('utf-8'))
                        file_bytes.name = f'Feedback_List_Part-{part}.csv'
                        list_file.append(file_bytes)
                        part += 1
                    
                    output = io.StringIO()
                    writer = csv.writer(output)

                    writer.writerow([
                        "feedback_rate", 
                        "feedback_body",
                        "created_at",
                    ])

                writer.writerow([
                    dt['feedback_rate'], 
                    dt['feedback_body'],
                    dt['created_at'],
                ])

            if output is not None:
                output.seek(0)
                res_output = output.getvalue() 
                file_bytes = io.BytesIO(res_output.encode('utf-8'))
                file_bytes.name = f'Feedback_List_Part-{part}.csv'
                list_file.append(file_bytes)

            if len(list_file) == 1:
                if admins:
                    for idx, dt in enumerate(admins):
                        await send_tele_chat(msg=f"[ADMIN] Hello {dt.username}, I just checked the feedback, and this is what I found. Im sending the audit to you in CSV format...",tele_id=dt.telegram_user_id, file_path=list_file[0])     
            else:     
                if admins:
                    for idx, dt in enumerate(admins):
                        await send_tele_chat(msg=f"[ADMIN] Hello {dt.username}, I just checked the feedback, and this is what I found. Im sending the audit to you in CSV format...\nSpliting into {len(list_file)} parts. Each of these have maximum 100 feedback",tele_id=dt.telegram_user_id)     
                        for idx, dt in enumerate(list_file):
                            await send_tele_chat(file_path=dt, msg=f"Part-{idx+1}\n",tele_id=dt.telegram_user_id)
            if admins:
                for idx, dt in enumerate(admins):
                    await send_tele_chat(msg=f"[ADMIN] Export finished",tele_id=dt.telegram_user_id)