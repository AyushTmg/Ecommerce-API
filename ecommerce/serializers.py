from .models import (
    Collection,
    Product,
)



from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


# !Collection Serializer
class CollectionSerializer(ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title']

# !Product Serializer
class ProductSerailizer(ModelSerializer):
    class Meta:
        model=Product
        fields=[
            'id'
            ,'title'
            ,'description'
            ,'price'
            ,'is_available'
            ,'collection'
        ]

    def create(self, validated_data):
        """ 
        Used for Creating a new product with the 
        validated data from the user and user_id
        context passed from ProductViewSet
        """
        user_id=self.context['user_id']
        return Product.objects.create(user_id=user_id,**validated_data)

