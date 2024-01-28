
# !Note : The following functions are used for testing and development phase!
# !Note : The following functions are used for testing and development phase!
# !Note : The following functions are used for testing and development phase!

from django.core.management.base import BaseCommand
from ...utils import (
    generate_dummy_collection,
    generate_dummy_user,
    generate_dummy_product,
    generate_dummy_review,
    generate_dummy_reply

)


class Command(BaseCommand):
    """ 
    Dummy Data Generating function is called 
    here when the command 'python manage.py dummydata' is run in terminal
    """

    help="Dummy Data Generating function is called here"

    def handle(self, *args,**kwargs) -> str :
        try:

            generate_dummy_user(10)
            generate_dummy_collection(10)
            generate_dummy_product(10)
            generate_dummy_review(10),
            generate_dummy_reply(10)

        except Exception as error:
            print("Error alert",error)

        else:
            print("Dummy Data Generated Successfully")

        