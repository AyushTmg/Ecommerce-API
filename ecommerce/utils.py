
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


 




