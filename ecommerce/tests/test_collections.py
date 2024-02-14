import pytest

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
)





# ! Tests Related to Anynomous User
@pytest.mark.django_db
class TestCollectionForAnynomousUsers:
  
    def test_if_user_is_anonymous_for_get_method_returns_200(
            self,
            get_method_fixture #Fixture
        ):
        """
        Test for checking if anynomous user when access 
        the collection endpoint gets the 200 OK status 
        or not 
        """
    
        # ! Fixture for get method is called
        response=get_method_fixture("/api/e-commerce/collections/")

        assert response.status_code == HTTP_200_OK
        

    def test_if_user_is_anonymous_for_post_request_returns_401(
            self,
            post_method_fixture #Fixture
        ):
        """
        Test for checking if anynomous users get the 401 Unauthorized 
        or not when perform post in collection endpoint 
        """
        
        # !Fixture for post method is called 
        response=post_method_fixture("/api/e-commerce/collections/",{"title":'a'})

        assert response.status_code == HTTP_401_UNAUTHORIZED


    def test_if_user_is_anynomous_for_delete_request_return_401(
            self,
            delete_method_fixture #Fixture
        ):
        """ 
        Test for returing 401 unauthorized if the users is
        anynomous and perform delete method on specific collection
        detail
        """
        
        # ! Fixture for delete method is called 
        response=delete_method_fixture("/api/e-commerce/collections/",99)

        assert response.status_code == HTTP_401_UNAUTHORIZED




# ! Tests Related to Authenticated Users
@pytest.mark.django_db
class TestCollectionsForAuthenticatedUsers:


    def test_if_user_is_authenticated_for_get_method_returns_200(
            self,
            get_method_fixture, #Fixture
            normal_user_authenticate_fixture #Fixture
        ):
        """
        Test for checking if authenticated user when access 
        the collection endpoint gets the 200 OK status 
        or not 
        """
        
        # ! Fixture for authenticating user as normal user is called 
        normal_user_authenticate_fixture()

        # ! Fixture for get method is called
        response=get_method_fixture("/api/e-commerce/collections/")

        assert response.status_code == HTTP_200_OK

    
    def test_if_user_is_authenticated_for_post_request_returns_401(
            self,
            post_method_fixture, #Fixture
            normal_user_authenticate_fixture #Fixture
        ):
        """
        Test for checking if authenticated users get the 401 Unauthorized 
        or not when perform post in collection endpoint 
        """

        # ! Fixture for authenticating user as normal user is called 
        normal_user_authenticate_fixture()

        # !Fixture for post method is called 
        response=post_method_fixture("/api/e-commerce/collections/",{"title":'a'})

        assert response.status_code == HTTP_403_FORBIDDEN


    def test_if_user_is_authenticated_for_delete_request_return_403(
            self,
            delete_method_fixture, #Fixture
            normal_user_authenticate_fixture #Fixture
        ):
        """ 
        Test for returing 403 forbidden if the authenticated 
        users perform delete method on collection detail
        """
        
        # ! Fixture for authenticating user as normal user is called 
        normal_user_authenticate_fixture()

        # ! Fixture for delete method is called 
        response=delete_method_fixture("/api/e-commerce/collections/",99)

        assert response.status_code == HTTP_403_FORBIDDEN
    



# ! Tests Related to Admin Users
@pytest.mark.django_db
class TestCollectionsForAdminUsers:

    def test_if_user_is_admin_for_get_request_returns_200(
            self,
            get_method_fixture, #Fixture
            admin_user_authenticate_fixture #Fixture
        ):
        """
        Test for checking if admin user get 200 OK 
        or not when request GET method in collection 
        endpoint 
        """
        
        # ! Fixture for authenticating user as admin is called 
        admin_user_authenticate_fixture()

        # ! Fixture for get method is called 
        response=get_method_fixture("/api/e-commerce/collections/")

        assert response.status_code == HTTP_200_OK


    def test_if_user_is_admin_for_post_request_returns_201(
            self,
            post_method_fixture, #Fixture
            admin_user_authenticate_fixture #Fixture
        ):
        """
        Test for checking if admin user get 201 CREATED 
        or not when perform post in collection endpoint 
        """

        # ! Fixture for authenticating user as admin is called 
        admin_user_authenticate_fixture()

        # ! Fixture for post method is called
        response=post_method_fixture("/api/e-commerce/collections/",{"title":'a'})

        # ! Using Multiple Assert for handeling exceptions 
        assert response.status_code == HTTP_201_CREATED
        assert response.data['title'] is not None 
        assert response.data['id']>0
        

    def test_if_user_is_admin_for_delete_request_return_404(
            self,
            delete_method_fixture, #Fixture
            admin_user_authenticate_fixture #Fixture
        ):
        """ 
        Test for returing 404 not found if the admin users
        perform delete method on collection detail
        """

        # ! Fixture for authenticating user as admin is called 
        admin_user_authenticate_fixture()
 
        # ! Fixture for delete method is called 
        response=delete_method_fixture("/api/e-commerce/collections/",99)

        assert response.status_code == HTTP_404_NOT_FOUND
        

    


    

