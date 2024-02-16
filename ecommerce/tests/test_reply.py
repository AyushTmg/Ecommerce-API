import pytest 

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED
)

from rest_framework.test import APIClient


# ! Test For Anynomous Users 
@pytest.mark.django_db
class TestReviewForAnynomousUser:
    
    def test_if_user_is_anynomous_for_get_method_return_200(
            self,
            post_method_fixture, #Fixture
            admin_user_authenticate_fixture,#Fixture
        ):
        """
        Returns 200 OK if anynomous user tries to perform
        GET method
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
        
        # ! For Using Anynomous user For GET method 
        client=APIClient()
        response= client.get(f"/api/e-commerce/products/{product_id}/reviews/{review_id}/replies/")

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
        response=post_method_fixture("/api/e-commerce/products/5/reviews/11/replies/",data)

        assert response.status_code==HTTP_401_UNAUTHORIZED


    def test_if_user_is_anynomous_for_delete_method_return_401(
            self,
            delete_method_fixture #Fixture
        ):
        """
        Test For Returning 401 Unauthorized error when a
        anynomous user tries to perform delete method
        """
        # ! Fixture for delete method is called 
        response=delete_method_fixture(f"/api/e-commerce/products/5/reviews/11/replies/",99)
        
        return response.status_code == HTTP_401_UNAUTHORIZED
 



# ! Test For Normal Users 
@pytest.mark.django_db
class TestReviewForNormalUser:
    
    def test_if_user_is_normal_user_for_get_method_return_200(
            self,
            get_method_fixture, #Fixture
            post_method_fixture, #Fixture
            admin_user_authenticate_fixture, #Fixture
            normal_user_authenticate_fixture, #Fixture
        ):
        """
        Returns 200 OK if normal user tries to perform
        GET method
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

        # ! Authenticating user and normal user 
        normal_user_authenticate_fixture()
        
        # ! GET method fixture getting review reply
        response= get_method_fixture(f"/api/e-commerce/products/{product_id}/reviews/{review_id}/replies/")

        assert response.status_code==HTTP_200_OK


    def test_if_user_is_normal_user_for_post_method_return_201(
            self,
            post_method_fixture, #Fixture
            admin_user_authenticate_fixture, #Fixture
            normal_user_authenticate_fixture, #Fixture
        ):
        """
        Test for returing 201 Created status when a normal user 
        perform post method in review reply endpoint
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

        # ! Data For Post method 
        data={
            'description':"This is a Reply"
        }
        
        # ! For authenticating user as normal user for post method 
        normal_user_authenticate_fixture()

        # ! GET method fixture getting review reply
        response= post_method_fixture(f"/api/e-commerce/products/{product_id}/reviews/{review_id}/replies/",data)

        assert response.status_code==HTTP_201_CREATED 


    def test_if_user_is_normal_user_for_delete_method_return_404(
            self,
            delete_method_fixture, #Fixture
            normal_user_authenticate_fixture, #Fixture
        ):
        """
        Returns 404  if normal user tries to perform
        delete method
        """

        # ! Fixture For authenticating user as normal user 
        normal_user_authenticate_fixture()

        # ! Delete method Fixture is called 
        response=delete_method_fixture(f"/api/e-commerce/products/1/reviews/1/replies/",99)

        assert response.status_code==HTTP_404_NOT_FOUND


    def test_if_normal_user_is_trying_to_delete_other_users_reply_return_403(
            self,
            post_method_fixture, # Fixture
            delete_method_fixture, #Fixture
            admin_user_authenticate_fixture, #Fixture
            normal_user_authenticate_fixture, #Fixture
        ):
        """
        Test for returning 403 if  an normal user tries to 
        delete another users's reply
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
        
        # ! Data for creating a reply
        reply_data={
            "description": "This is a reply"
        }

        # ! Using post method to create a reply
        reply=post_method_fixture(f"/api/e-commerce/products/{product_id}/reviews/{review_id}/replies/",reply_data)

        # ! Getting reply id from created reply
        reply_id=reply.data['id']

        # ! Authenticating normal user 
        normal_user_authenticate_fixture()

        # ! Trying the delete method in the review reply created by another user above
        response=delete_method_fixture(f"/api/e-commerce/products/{product_id}/reviews/{review_id}/replies/",reply_id)

        assert response.status_code==HTTP_403_FORBIDDEN




# ! Test For Admin Users 
@pytest.mark.django_db
class TestReviewForAdminUser:

    def test_if_user_is_admin_for_get_method_return_200(
            self,
            get_method_fixture, #Fixture
            post_method_fixture, #Fixture
            admin_user_authenticate_fixture, #Fixture
        ):
        """
        Returns 200 OK if admin user tries to perform
        GET method
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
        
        # ! GET method fixture getting review reply
        response= get_method_fixture(f"/api/e-commerce/products/{product_id}/reviews/{review_id}/replies/")

        assert response.status_code==HTTP_200_OK  


    def test_if_user_is_admin_for_post_method_return_201(
            self,
            post_method_fixture, # Fixture
            admin_user_authenticate_fixture # Fixture
        ):
        """  
        Test Method For Returing 201 Created when admin users
        perform post method on review endpoint
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

        # ! Data For Post method 
        data={
            'description':"This is a Reply"
        }
        
        # ! GET method fixture getting review reply
        response= post_method_fixture(f"/api/e-commerce/products/{product_id}/reviews/{review_id}/replies/",data)

        assert response.status_code==HTTP_201_CREATED 

    
    def test_if_user_is_admin_for_delete_method_return_404(
            self,
            delete_method_fixture, #Fixture
            admin_user_authenticate_fixture, #Fixture
        ):
        """
        Test For Returing 404 for admin user performing 
        delete method in review replies endpoint 
        """

        # ! For Authenticating user as admin 
        admin_user_authenticate_fixture()
 
        #  ! Using Delete method Fixture 
        response=delete_method_fixture(f"/api/e-commerce/products/1/reviews/1/replies/",99)

        assert response.status_code==HTTP_404_NOT_FOUND



