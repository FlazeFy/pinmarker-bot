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
        
        assert isinstance(dt['pin_name'], str)
        assert isinstance(dt['pin_coordinate'], str)
        assert isinstance(dt['pin_category'], str)

        if dt['pin_desc'] is not None:
            assert isinstance(dt['pin_desc'], str)
        if dt['pin_person'] is not None:
            assert isinstance(dt['pin_person'], str)