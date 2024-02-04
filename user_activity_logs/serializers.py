from rest_framework.serializers import ModelSerializer
from authentication.models import  User
from ecommerce.serializers import OrderSerializer,ReviewSerailizer



# ! User Activity Serializer 
class UserActivitySerializer(ModelSerializer):
    """
    serializer for the user activity model which contains
    field of order activites and review activites 
    """
    order=OrderSerializer(many=True)
    review=ReviewSerailizer(many=True)

    class Meta:
        model=User
        fields=[
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'order',
            'review'
        ]
