import requests

user_id = 'fcd3f23e-e5aa-11ee-892a-3216422910e9'
base_url = 'http://127.0.0.1:8000'

def test_get_all_pin_api():
    response = requests.get(f"{base_url}/api/v1/pin/{user_id}")
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"
    
    # Check the data in object
    for dt in data['data']:
        assert 'pin_name' in dt
        assert 'pin_desc' in dt
        assert 'pin_coordinate' in dt
        assert 'pin_category' in dt
        assert 'pin_person' in dt
        assert 'pin_address' in dt
        assert 'created_at' in dt
        assert 'last_visit' in dt
        assert 'total_visit' in dt
        
        assert isinstance(dt['pin_name'], str)
        assert isinstance(dt['pin_coordinate'], str)
        assert isinstance(dt['pin_category'], str)
        assert isinstance(dt['created_at'], str)
        assert isinstance(dt['total_visit'], int)
        assert isinstance(dt['total_visit'] >= 0,True)

        if dt['pin_desc'] is not None:
            assert isinstance(dt['pin_desc'], str)
        if dt['pin_person'] is not None:
            assert isinstance(dt['pin_person'], str)
        if dt['pin_address'] is not None:
            assert isinstance(dt['pin_address'], str)
        if dt['last_visit'] is not None:
            assert isinstance(dt['last_visit'], str)

def test_get_all_pin_export_api():
    response = requests.get(f"{base_url}/api/v1/pin_export/{user_id}")
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"
    
    # Check the data in object
    for dt in data['data']:
        assert 'pin_name' in dt
        assert 'pin_long' in dt
        assert 'pin_lat' in dt
        
        assert isinstance(dt['pin_name'], str)
        assert isinstance(dt['pin_long'], str)
        assert isinstance(dt['pin_lat'], str)

def test_get_pin_by_category_api():
    category = 'cafe'
    response = requests.get(f"{base_url}/api/v1/pin/{category}/{user_id}")
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"
    
    # Check the data in object
    for dt in data['data']:
        assert 'pin_name' in dt
        assert 'pin_desc' in dt
        assert 'pin_lat' in dt
        assert 'pin_long' in dt
        assert 'pin_person' in dt
        assert 'pin_address' in dt
        assert 'pin_call' in dt
        assert 'pin_email' in dt
        
        assert isinstance(dt['pin_name'], str)
        assert isinstance(dt['pin_lat'], str)
        assert isinstance(dt['pin_long'], str)

        if dt['pin_desc'] is not None:
            assert isinstance(dt['pin_desc'], str)
        if dt['pin_person'] is not None:
            assert isinstance(dt['pin_person'], str)
        if dt['pin_address'] is not None:
            assert isinstance(dt['pin_address'], str)
        if dt['pin_call'] is not None:
            assert isinstance(dt['pin_call'], str)
        if dt['pin_email'] is not None:
            assert isinstance(dt['pin_email'], str)

# For discord
def test_get_all_pin_v2_api():
    response = requests.get(f"{base_url}/api/v2/pin")
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"
    
    # Check the data in object
    for dt in data['data']:
        assert 'pin_name' in dt
        assert 'pin_desc' in dt
        assert 'pin_coordinate' in dt
        assert 'pin_category' in dt
        assert 'pin_person' in dt
        assert 'pin_call' in dt
        assert 'pin_email' in dt
        assert 'pin_address' in dt
        assert 'created_at' in dt
        assert 'created_by' in dt
        assert 'is_global_shared' in dt
        
        assert isinstance(dt['pin_name'], str)
        assert isinstance(dt['pin_coordinate'], str)
        assert isinstance(dt['pin_category'], str)
        assert isinstance(dt['created_at'], str)
        assert isinstance(dt['created_by'], str)
        assert isinstance(dt['is_global_shared'], bool)

        if dt['pin_desc'] is not None:
            assert isinstance(dt['pin_desc'], str)
        if dt['pin_person'] is not None:
            assert isinstance(dt['pin_person'], str)
        if dt['pin_address'] is not None:
            assert isinstance(dt['pin_address'], str)
        if dt['pin_call'] is not None:
            assert isinstance(dt['pin_call'], str)
        if dt['pin_email'] is not None:
            assert isinstance(dt['pin_email'], str)

def test_get_nearest_pin_api():
    lat = "-6.2333934867861975"
    long = "106.82363788271587"
    payload = {
        "user_id": "fcd3f23e-e5aa-11ee-892a-3216422910e9",
        "max_distance": 5000,
        "limit": 5
    }

    response = requests.post(f"{base_url}/api/v1/pin/nearest/{lat}/{long}",json=payload)
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be an object"

    # Check is_found_near key in object body
    assert 'is_found_near' in data 
    assert isinstance(data['is_found_near'], bool), "The key 'is_found_near' should be a bool"
    
    # Check the data in object
    for dt in data['data']:
        assert 'pin_name' in dt
        assert 'pin_coor' in dt
        assert 'distance' in dt
        
        assert isinstance(dt['pin_name'], str)
        assert isinstance(dt['pin_coor'], str)
        assert isinstance(dt['distance'], float)

def test_get_global_pin_by_list_id_api():
    payload = {
        "list_ids": "e396661c-5797-11ef-a5a5-3216422910e8,e39fa3c5-14d4-7ac9-1062-33e5d71ee72b",
    }
    response = requests.post(f"{base_url}/api/v1/pin_global/search/by_list_id", json=payload)
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"
    
    # Check the data in object
    for dt in data['data']:
        assert 'list_id' in dt
        assert 'list_name' in dt
        assert 'pin_name' in dt
        assert 'pin_category' in dt
        assert 'pin_coordinate' in dt
        assert 'created_at' in dt
        assert 'created_by' in dt
        
        assert isinstance(dt['list_id'], str)
        assert isinstance(dt['list_name'], str)
        assert isinstance(dt['pin_name'], str)
        assert isinstance(dt['pin_coordinate'], str)
        assert isinstance(dt['pin_category'], str)
        assert isinstance(dt['created_at'], str)
        assert isinstance(dt['created_by'], str)

def test_get_global_list_api():
    search = 'jakarta'
    response = requests.get(f"{base_url}/api/v1/pin_global/{search}")
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"
    
    # Check the data in object
    for dt in data['data']:
        assert 'id' in dt
        assert 'pin_list' in dt
        assert 'total' in dt
        assert 'list_name' in dt
        assert 'list_desc' in dt
        assert 'list_tag' in dt
        assert 'created_at' in dt
        assert 'created_by' in dt
        
        assert isinstance(dt['id'], str)
        assert isinstance(dt['pin_list'], str)
        assert isinstance(dt['total'], int)
        assert isinstance(dt['list_name'], str)
        assert isinstance(dt['created_at'], str)
        assert isinstance(dt['created_by'], str)

        if dt['list_desc'] is not None:
            assert isinstance(dt['list_desc'], str)
        if dt['list_tag'] is not None:
            assert isinstance(dt['list_tag'], list)

def test_get_pin_detail_history_by_id_api():
    pin_id = '049f5af1-7a22-4fea-adc3-dae717a45581'
    user_id = 'fcd3f23e-e5aa-11ee-892a-3216422910e9'
    response = requests.get(f"{base_url}/api/v1/pin/detail/{pin_id}/{user_id}")
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"

    # Check history key in object body
    assert 'history' in data
    assert isinstance(data['history'], list), "The key 'history' should be a array"

    # Check the data in object
    assert 'pin_name' in data['data']
    assert 'pin_desc' in data['data']
    assert 'pin_category' in data['data']
    assert 'pin_lat' in data['data']
    assert 'pin_long' in data['data']
    assert 'pin_person' in data['data']
    assert 'pin_email' in data['data']
    assert 'pin_call' in data['data']
    assert 'pin_address' in data['data']
    assert 'created_at' in data['data']
    assert 'updated_at' in data['data']
    
    assert isinstance(data['data']['pin_name'], str)
    assert isinstance(data['data']['pin_category'], str)
    assert isinstance(data['data']['pin_lat'], str)
    assert isinstance(data['data']['pin_long'], str)
    assert isinstance(data['data']['created_at'], str)

    if data['data']['pin_desc'] is not None:
        assert isinstance(data['data']['pin_desc'], str)
    if data['data']['pin_person'] is not None:
        assert isinstance(data['data']['pin_person'], str)
    if data['data']['pin_email'] is not None:
        assert isinstance(data['data']['pin_email'], str)
    if data['data']['pin_call'] is not None:
        assert isinstance(data['data']['pin_call'], str)
    if data['data']['pin_address'] is not None:
        assert isinstance(data['data']['pin_address'], str)
    if data['data']['updated_at'] is not None:
        assert isinstance(data['data']['updated_at'], str)

    # Check the history item in array
    for dt in data['history']:
        assert 'visit_desc' in dt
        assert 'visit_by' in dt
        assert 'visit_with' in dt
        assert 'created_at' in dt
        
        assert isinstance(dt['visit_by'], str)
        assert isinstance(dt['created_at'], str)

        if dt['visit_desc'] is not None:
            assert isinstance(dt['visit_desc'], str)
        if dt['visit_with'] is not None:
            assert isinstance(dt['visit_with'], str)

def test_get_pin_distance_to_my_personal_pin_by_id():
    pin_id = '049f5af1-7a22-4fea-adc3-dae717a45581'
    response = requests.get(f"{base_url}/api/v1/pin/distance/personal/{pin_id}/{user_id}")
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"
    
    # Check the data in object
    for dt in data['data']:
        assert 'id' in dt
        assert 'pin_name' in dt
        assert 'pin_desc' in dt
        assert 'pin_lat' in dt
        assert 'pin_long' in dt
        assert 'distance_to_meters' in dt
        assert 'created_at' in dt
        
        assert isinstance(dt['id'], str)
        assert isinstance(dt['pin_name'], str)
        assert isinstance(dt['pin_lat'], str)
        assert isinstance(dt['pin_long'], str)
        assert isinstance(dt['distance_to_meters'], float)
        assert isinstance(dt['created_at'], str)

        if dt['pin_desc'] is not None:
            assert isinstance(dt['pin_desc'], str)