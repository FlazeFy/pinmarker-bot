import requests

tele_id = '1317625977'
base_url = 'http://127.0.0.1:8000'

def test_get_user_by_tele_id_api():
    response = requests.get(f"{base_url}/api/v1/user/check/{tele_id}")
    data = response.json()

    # Check the status code
    assert response.status_code == 200    

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check data key in object body
    assert 'data' in data
    assert isinstance(data['data'], object), "The key 'data' should be a object"

    # Check role key in object body
    assert 'role' in data
    assert isinstance(data['role'], object), "The key 'role' should be a object"

    # Check is_found key in object body
    assert 'is_found' in data
    assert isinstance(data['is_found'], object), "The key 'is_found' should be a object"
    
    # Check the data in object
    assert 'id' in data['data']
    assert 'username' in data['data']
    assert 'email' in data['data']
    
    assert isinstance(data['data']['id'], str)
    assert isinstance(data['data']['username'], str)
    assert isinstance(data['data']['email'], str)

