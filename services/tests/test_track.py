import requests

user_id = 'fcd3f23e-e5aa-11ee-892a-3216422910e9'
base_url = 'http://127.0.0.1:8000'

def test_get_current_track():
    response = requests.get(f"{base_url}/api/v1/track/journey/{user_id}")
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
    for item in data['data']:
        assert 'battery_indicator' in item
        assert 'created_at' in item
        assert 'created_by' in item
        assert 'track_lat' in item
        assert 'track_long' in item
        assert 'track_type' in item
        
        assert isinstance(item['battery_indicator'], int)
        assert isinstance(item['created_at'], str)
        assert isinstance(item['created_by'], str)
        assert isinstance(item['track_lat'], float)
        assert isinstance(item['track_long'], float)
        assert isinstance(item['track_type'], str)

def test_get_last_track():
    response = requests.get(f"{base_url}/api/v1/track/last/{user_id}")
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
    assert 'battery_indicator' in data['data']
    assert 'created_at' in data['data']
    assert 'created_by' in data['data']
    assert 'track_lat' in data['data']
    assert 'track_long' in data['data']
    assert 'track_type' in data['data']
    
    assert isinstance(data['data']['battery_indicator'], int)
    assert isinstance(data['data']['created_at'], str)
    assert isinstance(data['data']['created_by'], str)
    assert isinstance(data['data']['track_lat'], float)
    assert isinstance(data['data']['track_long'], float)
    assert isinstance(data['data']['track_type'], str)

def test_get_total_distance_by_month():
    year = '2024'
    response = requests.get(f"{base_url}/api/v1/track/year/{year}/{user_id}")
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
    for item in data['data']:
        assert 'context' in item
        assert 'total' in item
        
        assert isinstance(item['context'], int)
        assert isinstance(item['total'], float)

    # Check data key in object body
    assert 'data_detail' in data
    assert isinstance(data['data_detail'], object), "The key 'data_detail' should be a object"
    
    # Check the data in object
    for item in data['data_detail']:
        assert 'created_at' in item
        assert 'month' in item
        
        assert isinstance(item['created_at'], str)
        assert isinstance(item['month'], int)

def test_get_total_distance_by_time():
    year = '2024'
    response = requests.get(f"{base_url}/api/v1/track/hour/{year}/{user_id}")
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
    for item in data['data']:
        assert 'context' in item
        assert 'total' in item
        
        assert isinstance(item['context'], int)
        assert isinstance(item['total'], float)

    # Check data key in object body
    assert 'data_detail' in data
    assert isinstance(data['data_detail'], object), "The key 'data_detail' should be a object"
    
    # Check the data in object
    for item in data['data_detail']:
        assert 'created_at' in item
        assert 'hour' in item
        
        assert isinstance(item['created_at'], str)
        assert isinstance(item['hour'], int)

def test_get_track_journey():
    payload = {
        "start_time": "2024-06-10T10:20:00",
        "end_time": "2024-06-10T10:30:00"
    }
    response = requests.post(f"{base_url}/api/v1/track/journey/period/{user_id}", json=payload)
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
    for item in data['data']:
        assert 'battery_indicator' in item
        assert 'created_at' in item
        assert 'created_by' in item
        assert 'track_lat' in item
        assert 'track_long' in item
        assert 'track_type' in item
        
        assert isinstance(item['battery_indicator'], int)
        assert isinstance(item['created_at'], str)
        assert isinstance(item['created_by'], str)
        assert isinstance(item['track_lat'], float)
        assert isinstance(item['track_long'], float)
        assert isinstance(item['track_type'], str)