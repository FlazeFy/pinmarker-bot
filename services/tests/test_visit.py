import requests

user_id = 'fcd3f23e-e5aa-11ee-892a-3216422910e9'
base_url = 'http://127.0.0.1:8000'

def test_get_all_visit_api():
    response = requests.get(f"{base_url}/api/v1/visit/{user_id}")
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"
    
    # Check the data in array
    for dt in data['data']:
        assert 'id' in dt
        assert 'pin_name' in dt
        assert 'visit_by' in dt
        assert 'visit_with' in dt
        assert 'visit_desc' in dt
        assert 'created_at' in dt
        
        assert isinstance(dt['id'], str)
        assert isinstance(dt['visit_by'], str)
        assert isinstance(dt['created_at'], str)

        if dt['visit_desc'] is not None:
            assert isinstance(dt['visit_desc'], str)
        if dt['visit_with'] is not None:
            assert isinstance(dt['visit_with'], str)
        if dt['pin_name'] is not None:
            assert isinstance(dt['pin_name'], str)

def test_get_all_visit_last_day_api():
    days = "all"
    response = requests.get(f"{base_url}/api/v1/visit/history/{user_id}/{days}")
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"
    
    # Check the data in array
    for dt in data['data']:
        assert 'pin_name' in dt
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
        if dt['pin_name'] is not None:
            assert isinstance(dt['pin_name'], str)
