import re

def validate_data(data, field_name: str, field_type: str, max_length: int = None, min_length: int = None, is_required: bool = False):
    res = []

    if data is not None:
        if field_type == 'string' and not isinstance(data, str):
            res.append({
                "field":field_name,
                "message":f"{field_name} must be a text"
            })
        elif field_type == 'integer' and not isinstance(data, int):
            res.append({
                "field":field_name,
                "message":f"{field_name} must be a number"
            })
        elif field_type == 'array' and not isinstance(data, list):
            res.append({
                "field":field_name,
                "message":f"{field_name} must be a list"
            })
        elif field_type == 'object' and not isinstance(data, object):
            res.append({
                "field":field_name,
                "message":f"{field_name} must be an object"
            })
        
        if field_type == 'string' or field_type == 'integer' or field_type == 'array':
            if max_length != None and len(data) > max_length:
                res.append({
                    "field":field_name,
                    "message":f"{field_name} exceeds maximum length of {max_length} characters"
                })
            if min_length != None and len(data) < min_length:
                res.append({
                    "field":field_name,
                    "message":f"{field_name} is shorter than minimum length of {min_length} characters"
                })
    elif is_required and data is None:
        res.append({
            "field":field_name,
            "message":f"{field_name} cant be empty"
        })
    elif not is_required and data is None:
        res = None

    if res is not None and len(res) == 0:
        return None
    else:
        return res

def contains_item(text: str, items: list[str]) -> bool:
    return any(item in text for item in items)

def contains_link(text):
    url_pattern = r'(https?://\S+|www\.\S+)'
    return re.search(url_pattern, text) is not None
