from django.dispatch import Signal,receiver
from .tasks import send_order_email_confirmation_task
order_created=Signal()


@receiver(order_created)
def on_order(sender,**kwargs):
    """
    Custome Signal which is executed when an order is 
    created
    """
    # ! This data is to inform the user that order has been placed  
    data_for_sending_mail_to_customer={
          'user':kwargs['order'].user,
          'to_email':kwargs['order'].user.email,
          'subject':"Order Placed"
    }
        
    # ! This data is to inform supplier about the order has been
    # ! placed and is assumed that all the product are sold by a
    # ! single supplier and the supplier email should be used in this
    data_for_sending_mail_to_suppliser={
        'user':kwargs['order'].user,
        'to_email':"thesupplier@gmail.com",
        'subject':"Order Received"
    }

    #! Calling a Celery Task for sending  email
    send_order_email_confirmation_task.delay(
        data_for_sending_mail_to_customer,
        data_for_sending_mail_to_suppliser
    )

