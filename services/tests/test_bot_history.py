import requests

tele_id = '1317625977'
base_url = 'http://127.0.0.1:8000'

def test_get_bot_history_api():
    response = requests.get(f"{base_url}/api/v1/bot_history/{tele_id}")
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
        assert 'command' in dt
        assert 'created_at' in dt
        assert 'total' in dt
        
        assert isinstance(dt['command'], str)
        assert isinstance(dt['created_at'], str)
        assert isinstance(dt['total'], int)