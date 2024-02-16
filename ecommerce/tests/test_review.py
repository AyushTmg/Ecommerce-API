import pytest 

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)

        


# ! Test Product Reviews For Anynomous Users
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
        Test Method which returns 401 Unauthorized status
        when a anynomous user perform POST method
        """

        data={
            "description": "This is a review "
        }
        
        # ! Fixture for post method is called 
        response=post_method_fixture(f"/api/e-commerce/products/{id}/reviews/",data)

        assert response.status_code==HTTP_401_UNAUTHORIZED


    def test_if_anynomous_for_delete_method_return_401(
            self,
            delete_method_fixture, #Fixture
        ):
        """
        Test for returning 401 status if when a anynomous
        user perform delete method on reviews endpoint
        """

        # ! Fixture for delete method is called 
        response=delete_method_fixture(f"/api/e-commerce/products/5/reviews/",99)
        
        return response.status_code == HTTP_401_UNAUTHORIZED
 





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
        Test Method which returns 201 Created status 
        when a normal user perform GET method
        """

        # ! Fixture For authenticating user as admin 
        admin_user_authenticate_fixture()

        # ! Creating a collection using post method fixture
        collection = post_method_fixture("/api/e-commerce/collections/",{"title":'a'})

        # ! Fixture for creating a product is called
        product=post_method_fixture(
            "/api/e-commerce/products/",
            {
                "title": "33",
                "description": "ss",
                "price": 99,
                "collection": collection.data['id'] #! Using id of created collection
            }
        )

        # ! created product id is stored 
        product_id=product.data['id']

        # ! Fixture for authenticating user as normal user
        normal_user_authenticate_fixture()

        # ! Data for passing to post fixture for creating a review
        data={
            "description": "This is a review "
        }

        # ! Fixture for post method is called for creating a product review
        # ! For the product created above
        response=post_method_fixture(f"/api/e-commerce/products/{product_id}/reviews/",data)

        assert response.status_code==HTTP_201_CREATED 


    def test_if_normal_user_for_delete_method_return_404(
            self,
            delete_method_fixture, #Fixture
            normal_user_authenticate_fixture #Fixture
        ):
        """
        Test for returning 404 Not Found Status if when a 
        authenticated user perform delete method on reviews endpoint
        """

        # ! Fixture for authenticating user as admin 
        normal_user_authenticate_fixture()

        # ! Fixture for delete method is called 
        response=delete_method_fixture(f"/api/e-commerce/products/5/reviews/",99)
        
        return response.status_code == HTTP_404_NOT_FOUND
    

    def test_if_normal_user_is_trying_to_delete_other_users_review_return_403(
            self,
            post_method_fixture, # Fixture
            delete_method_fixture, #Fixture
            admin_user_authenticate_fixture, #Fixture
            normal_user_authenticate_fixture, #Fixture
        ):
        """
        Test for returning 403 if  an authenticated user tries 
        to delete another users's review
        """

        # ! For Authenticating user as admin 
        admin_user_authenticate_fixture()

        # ! Creating a collection using post method fixture
        collection = post_method_fixture("/api/e-commerce/collections/",{"title":'a'})

        # ! Fixture for creating product
        response=post_method_fixture(
            "/api/e-commerce/products/",
            {
                "title": "33",
                "description": "ss",
                "price": 99,
                "collection": collection.data['id'] #! Using id of created collection
            }
        )

        # !For storing product id 
        product_id=response.data['id']

        # ! Data for passing to post fixture for creating review 
        data={
            "description": "This is a review "
        }
        # ! Fixture for creating a review is caled 
        review=post_method_fixture(f"/api/e-commerce/products/{product_id}/reviews/",data)

        # ! Created review id is stored
        review_id=review.data["id"]

        # ! Authenticating normal user 
        normal_user_authenticate_fixture()

        # ! Trying the delete method in the review created by another user above
        response=delete_method_fixture(f"/api/e-commerce/products/{product_id}/reviews/",review_id)

        assert response.status_code==HTTP_403_FORBIDDEN





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

        # ! Fixture for  Creating a Product
        product=post_method_fixture(
            "/api/e-commerce/products/",
            {
                "title": "33",
                "description": "ss",
                "price": 99,
                "collection": collection.data['id'] #! Using id of created collection
            }
        )
        
        # ! Created Product id is stored
        product_id=product.data['id']

        # ! Data for passing to post fixture for creating a review
        data={
            "description": "This is a review "
        }

        # ! Fixture for post method for creating review is called 
        response=post_method_fixture(f"/api/e-commerce/products/{product_id}/reviews/",data)

        assert response.status_code==HTTP_201_CREATED 


    def test_if_user_is_admin_for_delete_method_return_404(
            self,
            delete_method_fixture, #Fixture
            admin_user_authenticate_fixture #Fixture
        ):
        """
        Test for returning 404 Not Found Response if when a 
        admin user perform delete method on reviews endpoint
        """

        # ! Fixture for authenticating user as admin 
        admin_user_authenticate_fixture()

        # ! Fixture for delete method is called 
        response=delete_method_fixture(f"/api/e-commerce/products/5/reviews/",1)
        
        return response.status_code == HTTP_404_NOT_FOUND




 
        


