import pytest 

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND

)




# ! Tesing Product API for Anynomous Users
@pytest.mark.django_db
class TestProductForAnynomousUser:

    def test_if_user_is_anonymous_for_get_method_returns_200(
            self,
            get_method_fixture #Fixture
        ):
        """
        Test for checking if anynomous user when access 
        the product endpoint gets the 200 OK status 
        or not 
        """
    
        # ! Fixture for get method is called
        response=get_method_fixture("/api/e-commerce/products/")

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
        response=post_method_fixture(
            "/api/e-commerce/products/",
            {
                "title": "Product",
                "description": "Product Descriptions",
                "price": 11,
                #! If anynomous users could actually add a product then  this should be an existing collection id
                "collection": 1
            }
        )

        assert response.status_code == HTTP_401_UNAUTHORIZED


    def test_if_user_is_anynomous_for_delete_request_return_401(
            self,
            delete_method_fixture #Fixture
        ):
        """ 
        Test for returing 401 unauthorized if the users is
        anynomous and perform delete method on specific product
        detail
        """
        
        # ! Fixture for delete method is called 
        response=delete_method_fixture("/api/e-commerce/products/",99)

        assert response.status_code == HTTP_401_UNAUTHORIZED


    def test_if_user_is_anynomous_for_patch_method_return_401(
            self,
            patch_method_fixture, #Fixture
        ):
        """
        Test Method for returning 401 unauthorized if user is a
        anynomous and tries to perform  a patch request on product
        """
       
        product_id=99
        product_data={
            'title':"For this we dont need to pass exact data"
        }
 
        # ! Fixture for using patch method is called
        response=patch_method_fixture("/api/e-commerce/products/",product_id,product_data)

        assert response.status_code == HTTP_401_UNAUTHORIZED


    





# ! Tesing Product API for Normal Users
@pytest.mark.django_db
class TestProductForNormalUser:
    
    def test_if_user_is_normal_user_for_get_method_returns_200(
            self,
            get_method_fixture, #Fixture
            normal_user_authenticate_fixture #Fixture
        ):
        """
        Test for checking if authenticated user when access 
        the product endpoint gets the 200 OK status 
        or not 
        """
        
        # ! Fixture for authenticating user as normal user is called 
        normal_user_authenticate_fixture()

        # ! Fixture for get method is called
        response=get_method_fixture("/api/e-commerce/products/")

        assert response.status_code == HTTP_200_OK


    def test_if_user_is_normal_user_for_post_request_returns_401(
            self,
            post_method_fixture, #Fixture
            normal_user_authenticate_fixture, #Fixture
        ):
        """
        Test for checking if authenticated users get the 401 Unauthorized 
        or not when perform post in products endpoint 
        """

        # ! Fixture for authenticating user as normal user is called 
        normal_user_authenticate_fixture()


        # !Fixture for post method is called 
        response=post_method_fixture(
            "/api/e-commerce/products/",
            {
                "title": "Product",
                "description": "Product Descriptions",
                "price": 11,
                #! If authenticated users could actually add a product then  this should be an existing collection id
                "collection": 1 
            }
        )

        assert response.status_code == HTTP_403_FORBIDDEN


    def test_if_user_is_normal_user_for_delete_request_return_403(
            self,
            delete_method_fixture, #Fixture
            normal_user_authenticate_fixture#Fixture
        ):
        """ 
        Test for returing 403 forbidden if the normal authenticated 
        users perform delete method on product detail
        """
        
        # ! Fixture for authenticating user as normal user is called 
        normal_user_authenticate_fixture()


        # ! Fixture for delete method is called 
        response=delete_method_fixture("/api/e-commerce/products/",99)

        assert response.status_code == HTTP_403_FORBIDDEN


    def test_if_user_is_normal_user_for_patch_method_return_403(
            self,
            patch_method_fixture, #Fixture
            normal_user_authenticate_fixture #Fixture
        ): 
        """
        Test method for return status 403 Forbidden if a normal user tries 
        to use patch method for updating
        """

        # ! Fixture for authenticating user as normal user is called 
        normal_user_authenticate_fixture()

        product_id=99
        product_data={
            'title':"For this we dont need to pass exact data"
        }
 
        # ! Fixture for using patch method is called
        response=patch_method_fixture("/api/e-commerce/products/",product_id,product_data)

        assert response.status_code == HTTP_403_FORBIDDEN

        


# ! Tesing Product API for Admin Users
@pytest.mark.django_db
class TestProductForAdminUser:
    
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
        response=get_method_fixture("/api/e-commerce/products/")

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

        # ! Creating a collection using post method fixture
        collection = post_method_fixture("/api/e-commerce/collections/",{"title":'a'})

        # ! Fixture for post method is called
        response=post_method_fixture(
            "/api/e-commerce/products/",
            {
                "title": "33",
                "description": "33",
                "price": 99,
                "collection": collection.data['id'] #! Using id of created collection
            }
        )
        
        # ! Using Multiple Assert for handeling exceptions 
        assert response.status_code == HTTP_201_CREATED
        assert 'title' in response.data and response.data['title'] is not None
        assert 'description' in response.data and response.data['description'] is not None
        assert 'price' in response.data and isinstance(response.data['price'], int)
        assert 'collection' in response.data and response.data['collection'] is not None
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
            response=delete_method_fixture("/api/e-commerce/products/",99)

            assert response.status_code == HTTP_404_NOT_FOUND


    def test_if_user_is_admin_for_patch_method_return_200(
            self,
            patch_method_fixture, #Fixture
            post_method_fixture, #Fixture
            admin_user_authenticate_fixture #Fixture
        ):
        """ 
        Test Method for returning 200 OK response when a
        successful update is done
        """
 
        # ! Fixture for authentication user as admin is called
        admin_user_authenticate_fixture()
 
        # ! Here we have created a collection using post request
        collection_response = post_method_fixture("/api/e-commerce/collections/", {"title": 'a'})
        collection_id = collection_response.data['id']

        # ! Here we have created a product using post request and  added it to the collection
        product_response = post_method_fixture(
            "/api/e-commerce/products/",
            {
                "title": "33",
                "description": "33",
                "price": 99,
                "collection": collection_id 
            }
        )
        product_id = product_response.data['id']

        # ! Dictionary for Updaing the product fields
        updated_product_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "price": 199,
            "collection": collection_id
        }
 
        # ! Fixture for patch method is called to user patch method
        # ! on the created product in the created collection 
        response = patch_method_fixture("/api/e-commerce/products/", product_id, updated_product_data)

        # ! Multiple assertion for handeling exceptions 
        assert response.status_code == HTTP_200_OK
        assert 'title' in response.data and response.data['title'] is not None
        assert 'description' in response.data and response.data['description'] is not None
        assert 'price' in response.data and isinstance(response.data['price'], int)
        assert 'collection' in response.data and response.data['collection'] is not None
        assert response.data['id']>0




