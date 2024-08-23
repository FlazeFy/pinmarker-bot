import requests

base_url = 'http://127.0.0.1:8000'
search = 'jakarta'

def test_get_global_list_api():
    response = requests.get(f"{base_url}/api/v1/pin_global/{search}")
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
        assert 'id' in dt
        assert 'pin_list' in dt
        assert 'total' in dt
        assert 'list_name' in dt
        assert 'list_desc' in dt
        assert 'list_tag' in dt
        assert 'created_at' in dt
        assert 'created_by' in dt
        
        assert isinstance(dt['id'], str)
        assert isinstance(dt['pin_list'], str)
        assert isinstance(dt['total'], int)
        assert isinstance(dt['list_name'], str)
        assert isinstance(dt['created_at'], str)
        assert isinstance(dt['created_by'], str)

        if dt['list_desc'] is not None:
            assert isinstance(dt['list_desc'], str)
        if dt['list_tag'] is not None:
            assert isinstance(dt['list_tag'], list)