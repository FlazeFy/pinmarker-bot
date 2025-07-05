import requests

base_url = 'http://127.0.0.1:8000'

def test_post_check_bot_relation():
    payload = {
        "context_id": "C340248d16fc628bbd2c683261ja9j301",
        "relation_type": "group",
        "relation_platform": "line"
    }
    response = requests.post(f"{base_url}/api/v1/bot_relation/check", json=payload)
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
    assert 'context_id' in data['data']
    assert 'relation_type' in data['data']
    assert 'relation_platform' in data['data']
    assert 'relation_name' in data['data']
    assert 'created_at' in data['data']
    assert 'created_by' in data['data']
    assert 'expired_at' in data['data']
    assert 'username' in data['data']
    assert 'email' in data['data']
    
    assert isinstance(data['data']['context_id'], str)
    assert isinstance(data['data']['relation_type'], str)
    assert isinstance(data['data']['relation_platform'], str)
    assert isinstance(data['data']['relation_name'], str)
    assert isinstance(data['data']['created_at'], str)
    assert isinstance(data['data']['created_by'], str)
    assert isinstance(data['data']['expired_at'], str)
    assert isinstance(data['data']['username'], str)
    assert isinstance(data['data']['email'], str)

context_id = "123456789"
def test_post_create_bot_relation():
    payload = {
        "context_id": context_id,
        "relation_type": "group",
        "relation_platform": "line",
        "relation_name":"test"
    }
    response = requests.post(f"{base_url}/api/v1/bot_relation/create", json=payload)
    data = response.json()

    # Check the status code
    assert response.status_code == 201   

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
    
    # Check id key in object body
    assert 'id' in data
    assert isinstance(data['id'], str), "The key 'id' should be a object"

def test_post_sign_out_bot_relation():
    payload = {
        "context_id": context_id,
        "relation_type": "group",
        "relation_platform": "line",
    }
    response = requests.post(f"{base_url}/api/v1/bot_relation/sign_out", json=payload)
    data = response.json()

    # Check the status code
    assert response.status_code == 200   

    # Check message key in object body
    assert 'message' in data
    assert isinstance(data['message'], str), "The key 'message' should be an string"
