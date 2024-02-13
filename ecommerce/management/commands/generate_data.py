
# !Note : The following functions are used for testing and development phase!
# !Note : The following functions are used for testing and development phase!
# !Note : The following functions are used for testing and development phase!

from django.core.management.base import BaseCommand
from ...dummy import (
    generate_dummy_collection,
    generate_dummy_user,
    generate_dummy_product,
    generate_dummy_review,
    generate_dummy_reply,
    generate_dummy_cart,
    generate_dummy_order
)


class Command(BaseCommand):


    help="Dummy Data Generating function is called here"

    def handle(self, *args,**kwargs) -> str :
        """ 
        Dummy Data Generating function is called 
        here when the command 'python manage.py dummydata' is run in terminal
        """
        try:
            # Taking Inputs For number os records to generate
            num_of_user=int(input("Enter the number of dummy user's You want to generate\n"))
            num_of_collection=int(input("Enter the number of Collections's You want to generate\n"))
            num_of_product=int(input("Enter the number of product's You want to generate\n"))
            num_of_review=int(input("Enter the number of review's You want to generate\n"))
            num_of_reply=int(input("Enter the number of replie's You want to generate\n"))
            num_of_cart=int(input("Enter the number of cart and cart item's You want to generate\n"))
            num_of_order=int(input("Enter the number of order and order item's You want to generate\n"))

            # Callign dummy records generating functions with recived inputs
            generate_dummy_user(num_of_user)
            generate_dummy_collection(num_of_collection)
            generate_dummy_product(num_of_product)
            generate_dummy_review(num_of_review),
            generate_dummy_reply(num_of_reply)
            generate_dummy_cart(num_of_cart)
            generate_dummy_order(num_of_order)

        except Exception as error:
            print("Error alert",error)

        else:
            print("Dummy Data Generated Successfully")

        