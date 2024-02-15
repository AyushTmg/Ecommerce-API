import pytest 

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED
)

        


# ! Test Products For Anynomous Users
@pytest.mark.django_db
class TestProductReviewForAnynomousUser:

    def test_if_user_is_anynomous_for_get_method_return_200(
            self,
            get_method_fixture, #Fixture
        ):
        """
        Test Method which returns 200 OK response 
        when a anynomous user perform GET method
        """
        
        # ! Calling Fixture for get method 
        response=get_method_fixture("/api/e-commerce/products/1/reviews/")

        assert response.status_code==HTTP_200_OK


    def test_if_user_is_anynomous_for_post_method_return_401(
            self,
            post_method_fixture, #Fixture
        ):
        """
        Test Method which returns 200 OK response 
        when a normal user perform GET method
        """

        data={
            "description": "This is a review "
        }
        
        # ! Fixture for post method is called 
        response=post_method_fixture(f"/api/e-commerce/products/{id}/reviews/",data)

        assert response.status_code==HTTP_401_UNAUTHORIZED
 





# ! Test Products For Authenticated Users 
@pytest.mark.django_db
class TestProductReviewForNormalUser:

    def test_if_user_is_normal_user_for_get_method_return_200(
            self,
            get_method_fixture, #Fixture
            normal_user_authenticate_fixture #Fixture
        ):
        """
        Test Method which returns 200 OK response 
        when a normal user perform GET method
        """

        # ! Fixture for authenticating user as normal user
        normal_user_authenticate_fixture()

        # ! Fixture for GET Method is called 
        response=get_method_fixture("/api/e-commerce/products/1/reviews/")

        assert response.status_code==HTTP_200_OK


    def test_if_user_is_normal_user_for_post_method_return_201(
            self,
            post_method_fixture, #Fixture
            admin_user_authenticate_fixture, #Fixture
            normal_user_authenticate_fixture, #Fixture
        ):
        """
        Test Method which returns 200 OK response 
        when a normal user perform GET method
        """
        admin_user_authenticate_fixture()

        # ! Creating a collection using post method fixture
        collection = post_method_fixture("/api/e-commerce/collections/",{"title":'a'})

        # ! Fixture for post method is called
        response=post_method_fixture(
            "/api/e-commerce/products/",
            {
                "title": "33",
                "description": "ss",
                "price": 99,
                "collection": collection.data['id'] #! Using id of created collection
            }
        )
        id=response.data['id']
        # ! Fixture for authenticating user as normal user
        normal_user_authenticate_fixture()

        id=response.data['id']

        data={
            "description": "This is a review "
        }

        # ! Fixture for post method is called 
        response=post_method_fixture(f"/api/e-commerce/products/{id}/reviews/",data)

        assert response.status_code==HTTP_201_CREATED 






# ! Test Products For Admin Users 
@pytest.mark.django_db
class TestProductReviewForAdminUser:

    def test_if_user_is_admin_for_get_method_return_200(
            self,
            get_method_fixture, #Fixture
            admin_user_authenticate_fixture #Fixture
        ):
        """
        Test Method which returns 200 OK response 
        when a admin user perform GET method
        """

        # ! Fixture which authenticate user as admin user 
        admin_user_authenticate_fixture()

        # ! Fixture for GET method is called 
        response=get_method_fixture("/api/e-commerce/products/1/reviews/")
        
        assert response.status_code==HTTP_200_OK



    def test_if_user_is_admin_for_post_method_return_201(
            self,
            post_method_fixture, #Fixture
            admin_user_authenticate_fixture, #Fixture
        ):
        """
        Test for returning 201 Created Response when
        a admin user perform post method
        """
        admin_user_authenticate_fixture()

        # ! Creating a collection using post method fixture
        collection = post_method_fixture("/api/e-commerce/collections/",{"title":'a'})

        # ! Fixture for post method is called
        response=post_method_fixture(
            "/api/e-commerce/products/",
            {
                "title": "33",
                "description": "ss",
                "price": 99,
                "collection": collection.data['id'] #! Using id of created collection
            }
        )
        id=response.data['id']

        data={
            "description": "This is a review "
        }
        # ! Fixture for post method is called 
        response=post_method_fixture(f"/api/e-commerce/products/{id}/reviews/",data)

        assert response.status_code==HTTP_201_CREATED 



 
        


