
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings




class Util:
    @staticmethod
    def send_order_confirmation_to_customer(data):
        """
        For Sending Order Confirmation Email to customer
        """
        try:
            user_email = data['to_email']
            subject = data['subject']
            user=data['user']

            # ! For passing context in the template for email
            context={'user':user}

            message=render_to_string('emails/order_placed.html',context)
            send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email],html_message=message)

        except Exception as e:
            print(f"Some Error occrured during sending email {e}")


    @staticmethod
    def send_order_confirmation_to_supplier(data):
        """
        For Sending Order Confirmation Email to customer
        """
        try:
            # ! Email of Supplier called from setting.py 
            user_email =settings.SUPPLIER_EMAIL

            subject = data['subject']
            user=data['user']

            # ! For passing context in the template for email
            context={'user':user}
            
            message=render_to_string('emails/order_received.html',context)
            send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email],html_message=message)

        except Exception as e:
            print(f"Some Error occrured during sending email {e}") 



    @staticmethod
    def send_order_cancel_confirmatiom_to_user(data):
        """
        For Sending Order cancellation Confirmation
        to the user
        """
        try:
            user_email = data['to_email']
            subject = data['subject']
            user=data['user']

            # ! For passing context in the template for email
            context={'user':user}
            
            message=render_to_string('emails/order_cancellation_to_user.html',context)
            send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email],html_message=message)

        except Exception as e:
            print(f"Some Error occrured during sending email {e}") 



    @staticmethod
    def send_order_cancel_notification_to_supplier(data):
        """
        For Sending Order cancellation mail to the 
        supplier
        """

        try:
            # ! Email of Supplier called from setting.py 
            user_email =settings.SUPPLIER_EMAIL

            subject = data['subject']
            user=data['user']

            # ! For passing context in the template for email
            context={'user':user}
            
            message=render_to_string('emails/order_cancellation_to_supplier.html',context)
            send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email],html_message=message)

        except Exception as e:
            print(f"Some Error occrured during sending email {e}") 


   


# !Note : The following functions are used for testing and development phase!
# !Note : The following functions are used for testing and development phase!
# !Note : The following functions are used for testing and development phase!

from .models import (
    Collection,
    Product,
    Review,
    Reply,
    Order,
    OrderItem,
    Cart,
    CartItem
)


import random
from faker import Faker
from django.contrib.auth import get_user_model


User=get_user_model()
fake=Faker()


# !Function for generating dummy user
def generate_dummy_user(num):
    """
    Generate a specified number of dummy users for
    testing purpose.
    """
    for i in range(num):
        User.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            username=fake.user_name(),
            password=fake.password(),
        )



# !Function for generating dummy collection
def generate_dummy_collection(num):
    """
    generates dummy collections for testing purpose.
    """
    for i in range(num):
        Collection.objects.create(
            title=fake.word()
        )



# !Function for generating dummy product
def generate_dummy_product(num):
    """
    generates dummy product and realated collection 
    for testing purpose.
    """
    for i in range(num):
        id=random.randint(1,100)
        pk=random.randint(1,20)

        Product.objects.create(
            title=fake.word(),
            description=fake.text(max_nb_chars=50),
            price=random.uniform(10,100),
            user=User.objects.get(id=id),
            collection=Collection.objects.get(id=pk),
        )



# !Function for generating dummy review
def generate_dummy_review(num):
    """
    Generate a number of reviews related to existing
    products for testing purpose.
    """
    for i in range(num):
        user_id=random.randint(1,100)
        product_id=random.randint(1,100)

        Review.objects.create(
            description=fake.text(max_nb_chars=50),
            user=User.objects.get(id=user_id),
            product=Product.objects.get(id=product_id),
            time_stamp=fake.date_time_this_decade(),
        )



# !Function for generating dummy review reply
def generate_dummy_reply(num):
    """
    Adds replies to random reviews for testing purpose.
    """
    for i in range(num):
        user_id=random.randint(1,100)
        review_id=random.randint(1,100)

        Reply.objects.create(
            description=fake.text(max_nb_chars=50),
            user=User.objects.get(id=user_id),
            review=Review.objects.get(id=review_id),
            time_stamp=fake.date_time_this_decade(),
        )




# !Function for generating dummy Cart and cart Item record
def generate_dummy_cart(num):
    """
    Create dummy cart and cart item for
    testing purposes
    """
    for i in range(num):
        user_id=random.randint(1, 100) 
        product_id = random.randint(1, 100) 

        cart = Cart.objects.create(
            user=User.objects.get(id=user_id),
            time_stamp=fake.date_time_this_decade(),
        )

        CartItem.objects.create(
            quantity=random.randint(1, 15),
            cart=cart,
            product_id=product_id,
        )




# !Function for generating dummy order record
def generate_dummy_order(num):
    """
    Create dummy orders and order item for
    testing purposes
    """
    for i in range(num):
        user_id=random.randint(1, 100) 
        product_id = random.randint(1, 100) 

        order = Order.objects.create(
            user=User.objects.get(id=user_id),
            time_stamp=fake.date_time_this_decade(),
            payment_status=random.choice([Order.PENDING, Order.COMPLETE, Order.FAILED]),
        )

        OrderItem.objects.create(
            quantity=random.randint(1, 15),
            order=order,
            product_id=product_id,
            time_stamp=fake.date_time_this_decade(),
        )



# About Other Models Dummy Data
"""
Other data generations function will be added  at the 
time of working with their API's
"""




