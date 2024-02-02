from .utils import Util
from celery import shared_task


@shared_task(name='sending_order_confirmation_task')
def send_order_email_confirmation_task(data_for_customer,data_for_supplier):
    """
    This celery task call the two method of 
    sending mail to customer and supplier 
    about the order
    """
    try:
        Util.send_order_confirmation_to_customer(data_for_customer)
        Util.send_order_confirmation_to_supplier(data_for_supplier)
    except Exception as e:
        # ! For Dubugging purpose
        print(f"Some error on task.py {e}")
        
