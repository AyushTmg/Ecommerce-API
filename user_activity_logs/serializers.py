from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from authentication.models import  User
from ecommerce.serializers import OrderSerializer,ReviewSerailizer



# ! User Activity Serializer 
class UserActivitySerializer(ModelSerializer):
    """
    serializer for the user activity model which contains
    field of order activites and review activites 
    """
    order=OrderSerializer(many=True,read_only=True)
    review=ReviewSerailizer(many=True,read_only=True)
    email=serializers.EmailField(read_only=True)

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
