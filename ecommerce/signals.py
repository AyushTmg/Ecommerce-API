from .models import Cart
from .tasks import send_order_email_confirmation_task


from django.dispatch import Signal,receiver
from django.conf   import settings
from django.db.models import signals


# ! Custom Signal 
order_created=Signal()


# ! Signal Used when a Order is created 
@receiver(order_created)
def on_order(sender,**kwargs):
    """
    Custome Signal which is executed when an order is 
    created
    """
    # ! This data is to inform the user that order has been placed  
    data_for_sending_mail_to_customer={
          'user':str(kwargs['order'].user),
          'to_email':kwargs['order'].user.email,
          'subject':"Order Placed"
    }
        
    # ! This data is to inform supplier about the order has been
    # ! placed and is assumed that all the product are sold by a
    # ! single supplier 
    data_for_sending_mail_to_suppliser={
        'user':str(kwargs['order'].user),
        'subject':"Order Received"
    }

    #! Calling a Celery Task for sending  email
    send_order_email_confirmation_task.delay(
        data_for_sending_mail_to_customer,
        data_for_sending_mail_to_suppliser
    )



#! Signals Used when a user registers a account
@receiver(signals.post_save,sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender,**kwargs):
    """
    Whenever a User instance is save this function is 
    executed to create a associated cart for the user 
    """
    if kwargs['created']:
         Cart.objects.create(user=kwargs['instance'])