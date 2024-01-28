
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

def generate_dummy_collection(num):
    """
    generates dummy collections for testing purpose.
    """
    for i in range(num):
        Collection.objects.create(
            title=fake.word()
        )


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



# About Other Models Dummy Data
"""
Other data generations function will be added  at the 
time of working with their API's
"""


