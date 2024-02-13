import pytest 
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model



# ! This files contains Global fixtures for all the test 
# ! This files contains Global fixtures for all the test 
# ! This files contains Global fixtures for all the test 
# ! This files contains Global fixtures for all the test 



@pytest.fixture
def api_client():
    """
    Fixture to provide an instance of APIClient 
    for making requests to Django views in tests.
    """
    return APIClient()


@pytest.fixture
def user_authenticate_fixture(api_client):
    """
    Fixture to authenticate a user and make it 
    available globally.
    """
    def authenticate(is_staff=False):
        user_model = get_user_model()
        user = user_model.objects.create_user(username='test_user', email='test@example.com', password='password',is_staff=is_staff)
        return api_client.force_authenticate(user=user)
    
    return authenticate



@pytest.fixture
def get_method_fixture(api_client):
    """
    Fixture that returns an GET method globally
    with takes url parameter
    """
    def make_request(url):
        return api_client.get(url)
    
    return make_request




@pytest.fixture
def post_method_fixture(api_client):
    """
    Fixture that returns POST method globally,
    and take url and a dictionary as parameter
    """
    def make_request(url,val):
        return api_client.post(url,dict(val))
    
    return make_request




@pytest.fixture
def delete_method_fixture(api_client):
    """
    Fixture for DELETE and specific object 
    at the specific url which are required 
    as parameter
    """
    def  make_request(url,id):
        return api_client.delete(f"{url}{id}/")
    
    return make_request
