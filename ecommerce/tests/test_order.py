import pytest 

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,

)


# ! Test for Anynomous Users 
class TestOrderForAnynomousUser:

    def test_if_user_is_anynomous_for_get_method_return_401(
            self,
            get_method_fixture #Fixture
        ):
        """
        Test Method for returning 401 unauthorized status when 
        a anynomous user tries to GET order endpoint
        """

        # ! Fixture for get method is called
        response=get_method_fixture("/api/e-commerce/cart/")

        assert response.status_code==HTTP_401_UNAUTHORIZED
    
    




# ! Test for Authenticated Users 
@pytest.mark.django_db
class TestOrderForAuthenticatedUser:

    def test_if_user_is_normal_user_for_get_method_return_200(
            self,
            get_method_fixture, #Fixture
            normal_user_authenticate_fixture #Fixture

        ):
        """
        Test Method for returning 200 OK status when 
        normal user perform GET method in order endpoint
        """

        # ! Authenticating user as normal user 
        normal_user_authenticate_fixture()

        # ! Fixture for get method is called
        response=get_method_fixture("/api/e-commerce/order/")

        assert response.status_code==HTTP_200_OK


    




# ! Test for Admin Users 
@pytest.mark.django_db
class TestOrderForAdminUser:
        
    def test_if_user_is_admin_user_for_get_method_return_200(
            self,
            get_method_fixture, #Fixture
            admin_user_authenticate_fixture #Fixture

        ):
        """
        Test Method for returning 200 OK status when 
        admin user perform GET method in order endpoint
        """

        # ! Authenticating user as admin user 
        admin_user_authenticate_fixture()

        # ! Fixture for get method is called
        response=get_method_fixture("/api/e-commerce/order/")

        assert response.status_code==HTTP_200_OK 






    