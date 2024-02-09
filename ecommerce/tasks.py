from .utils import Util
from celery import shared_task


# ! Order Confirmation Task
@shared_task(name='sending_order_confirmation_task')
def send_order_email_confirmation_task(data_for_customer,data_for_supplier):
    """
    This celery task  which takes two argument and 
    call the two of method for sending mail to 
    customer and supplier about the order
    """
    try:
        # ! Caling the methods to send email to customer and supplier 
        Util.send_order_confirmation_to_customer(data_for_customer)
        Util.send_order_confirmation_to_supplier(data_for_supplier)
    except Exception as e:
        # ! For Dubugging purpose
        print(f"Some error on task.py {e}")




# ! Order Cancellation Task
@shared_task(name='order_cancellation_task')
def send_order_cancellation_email_task(data_for_customer,data_for_supplier):
    """
    This celery task is used to send an email to both
    customer and the supplier when an order is cancelled
    """
    try:
        # ! Caling the methods to send email to customer and supplier 
        Util.send_order_cancel_confirmatiom_to_user(data_for_customer)
        Util.send_order_cancel_notification_to_supplier(data_for_supplier)
    except Exception as e:
        # ! For Dubugging purpose
        print(f"Some error on task.py {e}")
        
