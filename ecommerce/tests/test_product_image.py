import pytest 

from rest_framework.status import (
    HTTP_200_OK,
)



# ! Test For Anynomous Users 
@pytest.mark.django_db
class TestProductImageForAnynomousUser:

    def test_if_user_is_anynomous_for_get_method_return_200(
            self,
            get_method_fixture, # Fixture
        ):
        """
        Test for returning 200 OK Response when user is
        anynomous 
        """
        # ! Fixture for calling GET method 
        response=get_method_fixture(f'/api/e-commerce/products/1/images/')
        assert response.status_code == HTTP_200_OK




# ! Test For Normal Users 
@pytest.mark.django_db
class TestProductImageForNormalUser:

    def test_if_user_is_normal_user_for_get_method_return_200(
            self,
            get_method_fixture, # Fixture
            normal_user_authenticate_fixture,  # Fixture
        ):
        """
        Test for returning 200 OK Response when  user is
        normal user 
        """

        # ! Fixture for authenticating user as normal user 
        normal_user_authenticate_fixture()

        # ! Fixture for calling GET method 
        response=get_method_fixture(f'/api/e-commerce/products/1/images/')

        assert response.status_code == HTTP_200_OK




# ! Test For Admin Users 
@pytest.mark.django_db
class TestProductImageForAdminUser:

    def test_if_user_is_admin_for_get_method_return_200(
            self,
            get_method_fixture, # Fixture
            admin_user_authenticate_fixture # Fixture
        ):
        """
        Test for returning 200 OK Response when user is
        anynomous 
        """
        # ! Fixture for authenticating user as admin user 
        admin_user_authenticate_fixture() 

        # ! Fixture for calling GET method 
        response=get_method_fixture(f'/api/e-commerce/products/1/images/')

        assert response.status_code == HTTP_200_OK





