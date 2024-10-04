import requests

user_id = 'fcd3f23e-e5aa-11ee-892a-3216422910e9'
base_url = 'http://127.0.0.1:8000'

def test_get_all_history_api():
    response = requests.get(f"{base_url}/api/v1/history/{user_id}")
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
        assert 'history_type' in dt
        assert 'history_context' in dt
        assert 'created_at' in dt
        
        assert isinstance(dt['id'], str)
        assert isinstance(dt['history_type'], str)
        assert isinstance(dt['history_context'], str)
        assert isinstance(dt['created_at'], str)
