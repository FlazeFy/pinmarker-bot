import requests

user_id = 'fcd3f23e-e5aa-11ee-892a-3216422910e9'
base_url = 'http://127.0.0.1:8000'

def test_get_all_dct_by_type_api():
    dct_type = 'pin_category'
    response = requests.get(f"{base_url}/api/v1/dct/{dct_type}/{user_id}")
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
        assert 'dictionary_name' in dt
        assert 'dictionary_color' in dt
        
        assert isinstance(dt['dictionary_name'], str)
        assert isinstance(dt['dictionary_color'], str)
