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
def normal_user_authenticate_fixture(api_client):
    """
    Fixture to authenticate a user as normal user
    and make it available globally.
    """
    def authenticate():
        user_model = get_user_model()

        #!  Create Normal User
        user = user_model.objects.create_user(
            first_name="testname",
            last_name="testname",
            username='test_user',
            email='test@example.com',
            password='password'
        )

        return api_client.force_authenticate(user=user)
    
    return authenticate


@pytest.fixture
def admin_user_authenticate_fixture(api_client):
    """
    Fixture to authenticate a user as admin and 
    make it available globally.
    """
    def authenticate():
        user_model = get_user_model()

        # ! Create and authenticate admin user
        user = user_model.objects.create_user(
            first_name="testname",
            last_name="testname",
            username='user_admin',
            email='test_admin@example.com',
            password='password',
            is_staff=True
        )

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
def delete_method_fixture(api_client):
    """
    Fixture for DELETE and specific object 
    at the specific url which are required 
    as parameter
    """
    def  make_request(url,id):
        return api_client.delete(f"{url}{id}/")
    
    return make_request




@pytest.fixture
def put_method_fixture(api_client):
    """
    Fixture for PUT method for a specific
    object 
    """
    def make_request(url,val):
        return api_client.put(f"{url}",val)
    
    return make_request
    



    
