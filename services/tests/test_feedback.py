import requests

base_url = 'http://127.0.0.1:8000'

def test_get_feedback_api():
    response = requests.get(f"{base_url}/api/v1/feedback")
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
        assert 'feedback_rate' in dt
        assert 'feedback_body' in dt
        assert 'created_at' in dt
        
        assert isinstance(dt['feedback_rate'], int)
        assert isinstance(dt['feedback_body'], str)
        assert isinstance(dt['created_at'], str)
