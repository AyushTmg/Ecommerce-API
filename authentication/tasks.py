from celery import shared_task
from .utils import Util

@shared_task(name="activation_email")
def activation_email_task(data):
    """
    Sending account activation email task 
    """
    try:
        Util.send_activation_email(data)
    except Exception as e:
        print(f"An error occurred while running task --> {e}")

    
@shared_task(name="password_reset_email")
def password_reset_task(data):
    """
    Sending Password Reset email task 
    """
    try:
        Util.send_password_reset_email(data)
    except Exception as e:
        print(f"An error occurred while running task --> {e}")
    

