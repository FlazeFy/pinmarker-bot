import requests

user_id = 'fcd3f23e-e5aa-11ee-892a-3216422910e9'
base_url = 'http://127.0.0.1:8000'

def test_dashboard_route():
    role = 'user'
    response = requests.get(f"{base_url}/api/v1/stats/dashboard/{user_id}/{role}")
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
    assert 'total_marker' in data['data']
    assert 'total_favorite' in data['data']
    assert 'last_visit' in data['data']
    assert 'most_visit' in data['data']
    assert 'most_category' in data['data']
    assert 'last_added' in data['data']
    
    assert isinstance(data['data']['total_marker'], int)
    assert isinstance(data['data']['total_favorite'], int)
    assert isinstance(data['data']['last_visit'], str)
    assert isinstance(data['data']['most_visit'], str)
    assert isinstance(data['data']['most_category'], str)
    assert isinstance(data['data']['last_added'], str)

def test_get_total_pin_by_category():
    response = requests.get(f"{base_url}/api/v1/stats/total_pin_by_category/{user_id}")
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
        
        assert isinstance(item['context'], str)
        assert isinstance(item['total'], int)

def test_get_total_visit_by_category():
    response = requests.get(f"{base_url}/api/v1/stats/total_visit_by_category/{user_id}")
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
        
        assert isinstance(item['context'], str)
        assert isinstance(item['total'], int)

def test_get_total_visit_by_category_by_pin():
    pin_id = '049f5af1-7a22-4fea-adc3-dae717a45581'
    response = requests.get(f"{base_url}/api/v1/stats/total_visit_by_category/{user_id}/{pin_id}")
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
        
        assert isinstance(item['context'], str)
        assert isinstance(item['total'], int)

def test_get_total_gallery_by_pin():
    response = requests.get(f"{base_url}/api/v1/stats/total_gallery_by_pin/{user_id}")
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
        
        assert isinstance(item['context'], str)
        assert isinstance(item['total'], int)
