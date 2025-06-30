from firebase_admin import storage
from datetime import datetime

def upload_firebase_storage(user_id: str, context:str, data_type:str, res):
    # Firebase Storage
    bucket = storage.bucket()
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    fileName = f"{context}_list_{user_id}_{now_str}.{data_type}"
    blob = bucket.blob(f"generated_data/{context}/{fileName}")
    blob.upload_from_string(res, content_type=f"text/{data_type}")
    blob.make_public()
    download_url = blob.public_url 

    return download_url