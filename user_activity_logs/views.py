from authentication.models import User 
from .serializers import UserActivitySerializer


from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status  import HTTP_200_OK 
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.permissions import IsAdminUser,IsAuthenticated


from django_filters.rest_framework import DjangoFilterBackend




# ! User Activity ViewSet 
class UserActvityViewSet(ModelViewSet):

    http_method_names=['get','head','options','put','patch','delete']
    permission_classes=[IsAdminUser]
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]

    search_fields=['username','email','id']
    ordering_fields=['username','id']

        

    def get_queryset(self):
        """
        Method to over ride the queryset to return user activity
        of all the user in the database for admin user 
        """

        return User.objects.all().prefetch_related(
                'order',
                'order__order_item',
                'order__order_item__product',
                'order__order_item__product__product_image',
                'review'
                )
    
    # ! Serailizer Class 
    serializer_class=UserActivitySerializer
    

    # !Custom Action for normal user's 
    @action(detail = False,methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self,request):
        """
        Adding custom me action in the viewset to show the user activity
        of the logged in normal users 
        """

        user=self.request.user
        # ! Viewing the normal user activty logs 
        if self.request.method=='GET':
                user=User.objects.filter(id=user.id).prefetch_related(
                    'order',
                    'order__order_item',
                    'order__order_item__product',
                    'order__order_item__product__product_image',
                    'review'
                    )
                serializer=self.serializer_class(user,many=True)
                return Response(serializer.data,status=HTTP_200_OK)
        

        # ! Taking the data from the request and updating the noraml user instance
        if self.request.method=='PUT':
            serializer=self.serializer_class(user,data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data,status=HTTP_200_OK)
        


    

    
        

    
       