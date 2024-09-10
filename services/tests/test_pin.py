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
        
        assert isinstance(dt['pin_name'], str)
        assert isinstance(dt['pin_coordinate'], str)
        assert isinstance(dt['pin_category'], str)
        assert isinstance(dt['created_at'], str)

        if dt['pin_desc'] is not None:
            assert isinstance(dt['pin_desc'], str)
        if dt['pin_person'] is not None:
            assert isinstance(dt['pin_person'], str)
        if dt['pin_address'] is not None:
            assert isinstance(dt['pin_address'], str)

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
        "id": "fcd3f23e-e5aa-11ee-892a-3216422910e9",
        "max_distance": 1000
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