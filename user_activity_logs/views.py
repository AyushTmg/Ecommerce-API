from .serializers import UserActivitySerializer
from rest_framework.viewsets import ModelViewSet
from authentication.models import User 




# ! User Activity ViewSet 
class UserActvityViewSet(ModelViewSet):
    http_method_names=['get','head','options','put','patch','delete']
        

    def get_queryset(self):
        """
        Method to over ride the queryset ro return user activity
        based on logged in user roles 
        """

        # ! This runs if the user is admin or a staff member
        if (self.request.user.is_staff or self.request.user.is_superuser):
            return User.objects.all().prefetch_related(
                'order',
                'order__order_item',
                'order__order_item__product',
                'order__order_item__product__product_image',
                'review'
                )
        

        # ! else  this is executed when user is a normal user 
        return User.objects.filter(id=self.request.user.id).prefetch_related(
                'order',
                'order__order_item',
                'order__order_item__product',
                'order__order_item__product__product_image',
                'review'
                )
    
        
    serializer_class=UserActivitySerializer

    
       