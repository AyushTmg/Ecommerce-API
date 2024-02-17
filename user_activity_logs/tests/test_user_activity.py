import pytest 

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND

)


# ! Test for Anynomous Users 
class TestUserActivityForAnynomousUser:

    def test_if_user_is_anynomous_for_get_method_return_401(
            self,
            get_method_fixture #Fixture
        ):
        """
        Test Method for returning 401 unauthorized status when 
        a anynomous user tries to GET user activity endpoint
        """

        # ! Fixture for get method is called
        response=get_method_fixture("/api/user/")

        assert response.status_code==HTTP_401_UNAUTHORIZED


    def test_if_user_is_anynomous_for_getting_profile_with_activities_return_200(
            self,
            get_method_fixture,  #Fixture
        ):
        """
        Test for returing 401 unauthorized status when a anynomous
        user tries access their profile with thier activities
        """

        # ! Fixture for get method is called
        response=get_method_fixture("/api/user/me/")

        assert response.status_code==HTTP_401_UNAUTHORIZED


    


# ! Test for Authenticated Users 
@pytest.mark.django_db
class TestUserActivityForAuthenticatedUser:

    def test_if_user_is_normal_user_for_get_method_return_200(
            self,
            get_method_fixture, #Fixture
            normal_user_authenticate_fixture #Fixture

        ):
        """
        Test Method for returning 403 Forbiddedn status when 
        normal user perform GET method in user activity endpoint
        """

        # ! Authenticating user as normal user 
        normal_user_authenticate_fixture()

        # ! Fixture for get method is called
        response=get_method_fixture("/api/user/")

        assert response.status_code==HTTP_403_FORBIDDEN 


    def test_if_user_is_normal_user_for_getting_profile_with_activities_return_200(
            self,
            get_method_fixture,  #Fixture
            normal_user_authenticate_fixture  #Fixture
        ):
        """
        Test for returing 200 OK status when a normal user tries 
        access their profile with thier activities
        """

        # ! Authenticating user as normal user 
        normal_user_authenticate_fixture()

        # ! Fixture for get method is called
        response=get_method_fixture("/api/user/me/")

        assert response.status_code==HTTP_200_OK 


    def test_if_user_is_normal_user_for_updating_thier_profile_return_200(
            self,
            put_method_fixture, #Fixture
            normal_user_authenticate_fixture, #Fixture
        ):
        """
        Test for returing 200 Ok Status when a normal user 
        update thier profile info
        """

        # ! Authenticating user as normal user 
        normal_user_authenticate_fixture()

        data={
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
            "username": "Updated Username"
        }
        # ! Fixture for put method is called for updating 
        response=put_method_fixture("/api/user/me/",data)

        assert response.status_code==HTTP_200_OK 



    

# ! Test for Admin Users 
@pytest.mark.django_db
class TestUserActivityForAdminUser:
        
    def test_if_user_is_admin_user_for_get_method_return_200(
            self,
            get_method_fixture, #Fixture
            admin_user_authenticate_fixture #Fixture

        ):
        """
        Test Method for returning 200 OK status when 
        admin user perform GET method in user activity endpoint
        """

        # ! Authenticating user as admin user 
        admin_user_authenticate_fixture()

        # ! Fixture for get method is called
        response=get_method_fixture("/api/user/")

        assert response.status_code==HTTP_200_OK 


    def test_if_user_is_admin_user_for_getting_profile_with_activities_return_200(
            self,
            get_method_fixture,  #Fixture
            normal_user_authenticate_fixture  #Fixture
        ):
        """
        Test for returing 200 OK status when a admin user tries 
        access their profile with thier activities
        """

        # ! Authenticating user as admin user 
        normal_user_authenticate_fixture()

        # ! Fixture for get method is called
        response=get_method_fixture("/api/user/me/")
        
        assert response.status_code==HTTP_200_OK 

    
    def test_if_user_is_admin_user_for_updating_thier_profile_return_200(
            self,
            put_method_fixture, #Fixture
            admin_user_authenticate_fixture, #Fixture
        ):
        """
        Test for returing 200 Ok Status when a admin user 
        update thier profile info
        """

        # ! Authenticating user as admin user 
        admin_user_authenticate_fixture()

        data={
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
            "username": "Updated Username"
        }
        # ! Fixture for put method is called for updating 
        response=put_method_fixture("/api/user/me/",data)

        assert response.status_code==HTTP_200_OK 

        
    def test_if_user_admin_user_for_delete_method_return_404(
            self,
            delete_method_fixture,
            admin_user_authenticate_fixture
        ):
        """
        Test For Returing 404 Not Found status when admin 
        user perform delete method 
        """

        # ! Authenticating user as admin user 
        admin_user_authenticate_fixture()

        # ! Fixture For delete method is called 
        response=delete_method_fixture("/api/user/",2)

        assert response.status_code==HTTP_404_NOT_FOUND


            
    
     