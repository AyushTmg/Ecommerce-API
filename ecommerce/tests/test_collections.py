import pytest

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
)

from django.contrib.auth.models import User




# ! Tests Related to Anynomous User
@pytest.mark.django_db
class TestCollectionForAnynomousUsers:
  
    def test_if_user_is_anonymous_for_get_method_returns_200(self,get_method_fixture):
        """
        Test for checking if anynomous user when access 
        the collection endpoint gets the 200 OK status 
        or not 
        """
    
        # ! Fixture for getting a collections called 
        response=get_method_fixture("/api/e-commerce/collections/")

        assert response.status_code == HTTP_200_OK
        

    def test_if_user_is_anonymous_for_post_request_returns_401(self,post_method_fixture):
        """
        Test for checking if anynomous users get the 401 Unauthorized 
        or not when perform post in collection endpoint 
        """
        
        # !Fixture for creating a collection called 
        response=post_method_fixture("/api/e-commerce/collections/",{"title":'a'})

        assert response.status_code == HTTP_401_UNAUTHORIZED


    def test_if_user_is_anynomous_for_delete_request_return_401(self,delete_method_fixture):
        """ 
        Test for returing 401 unauthorized if the users is
        anynomous and perform delete method on specific collection
        detail
        """
        
        # ! Fixture for deleting a specific collection called 
        response=delete_method_fixture("/api/e-commerce/collections/",99)

        assert response.status_code == HTTP_401_UNAUTHORIZED




# ! Tests Related to Authenticated Users
@pytest.mark.django_db
class TestCollectionsForAuthenticatedUsers:


    def test_if_user_is_authenticated_for_get_method_returns_200(self,user_authenticate_fixture,get_method_fixture):
        """
        Test for checking if authenticated user when access 
        the collection endpoint gets the 200 OK status 
        or not 
        """
        
        # ! Calling user_authenticate fixture for authenticating a user
        # ! Fixture for authenticating user is called 
        user_authenticate_fixture()

        # ! Fixture for getting a collections called 
        response=get_method_fixture("/api/e-commerce/collections/")

        assert response.status_code == HTTP_200_OK

    
    def test_if_user_is_authenticated_for_post_request_returns_401(self,user_authenticate_fixture,post_method_fixture):
        """
        Test for checking if authenticated users get the 401 Unauthorized 
        or not when perform post in collection endpoint 
        """

        # ! Fixture for authenticating user is called 
        user_authenticate_fixture()

        # !Fixture for post method is called 
        response=post_method_fixture("/api/e-commerce/collections/",{"title":'a'})

        assert response.status_code == HTTP_403_FORBIDDEN



    def test_if_user_is_authenticated_for_delete_request_return_403(self,user_authenticate_fixture,delete_method_fixture):
        """ 
        Test for returing 403 forbidden if the authenticated 
        users perform delete method on collection detail
        """
        # ! Fixture for authenticating user is called 
        user_authenticate_fixture()

        # ! Fixture for deleting a specific collection called 
        response=delete_method_fixture("/api/e-commerce/collections/",99)

        assert response.status_code == HTTP_403_FORBIDDEN
    




# ! Tests Related to Admin Users
@pytest.mark.django_db
class TestCollectionsForAdminUsers:

    def test_if_user_is_admin_for_get_request_returns_200(self):
        """
        Test for checking if admin user get 200 OK 
        or not when request GET method in collection 
        endpoint 
        """

        client=APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response=client.get("/api/e-commerce/collections/")
        

        assert response.status_code == HTTP_200_OK


    def test_if_user_is_admin_for_post_request_returns_201(self):
        """
        Test for checking if admin user get 201 CREATED 
        or not when perform post in collection endpoint 
        """

        client=APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response=client.post("/api/e-commerce/collections/",{"title":'a'})

        assert response.status_code == HTTP_201_CREATED
        

    def test_if_user_is_admin_for_delete_request_return_404(self):
        """ 
        Test for returing 404 not found if the admin users
        perform delete method on collection detail
        """

        # ! This is non existing collection id 
        collection_id=99

        client=APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response=client.delete(f"/api/e-commerce/collections/{collection_id}/")

        assert response.status_code == HTTP_404_NOT_FOUND
        

    


    

