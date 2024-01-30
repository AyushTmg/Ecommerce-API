from .models import (
    Collection,
    Product,
    ProductImage,
    Review,
    Reply,
    Cart,
    CartItem
)



from rest_framework import serializers
from rest_framework.serializers import ModelSerializer




# !Collection Serializer
class CollectionSerializer(ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title']




# !Product Image Serializer
class ProductImageSerializer(ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['image']
    
    def create(self, validated_data):
        """
        Create and return a new product image given 
        the validated data with the product_id 
        passed from the ProductImageSerializer
        """
        product_id=self.context['product_id']

        return (
            ProductImage.objects.create(
                product_id=product_id,
                **validated_data
                )
            )




# !Product Serializer
class ProductSerailizer(ModelSerializer):
    product_image=ProductImageSerializer(many=True,read_only=True)
    is_available=serializers.BooleanField(default=True,read_only=True)

    class Meta:
        model=Product
        fields=[
            'id'
            ,'title'
            ,'description'
            ,'price'
            ,'is_available'
            ,'collection',
            'product_image'
        ]


    def create(self, validated_data):
        """ 
        Used for Creating a new product with the 
        validated data from the user and user_id
        context passed from ProductViewSet
        """
        user_id=self.context['user_id']

        return (
            Product.objects.create(
                user_id=user_id,
                **validated_data
                )
        )




# !  Review Seriailzer 
class ReviewSerailizer(ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        fields=[
            'id',
            'user',
            'description',
            'time_stamp'
        ]


    def create(self, validated_data):
        """ 
        Used for Creating a new product with the 
        validated data from the user and user_id
        and product_id context passed from 
        ReviewViewSet
        """

        user_id=self.context['user_id']
        product_id=self.context['product_id']

        return (
            Review.objects.create(
                user_id=user_id,
                product_id=product_id,
                )
            )




# !Reply Serializer
class ReplySerializer(ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Reply
        fields=[
            'id',
            'user',
            'description',
            'time_stamp'
        ]


    def create(self, validated_data):
        """ 
        Used for Creating a new product with the 
        validated data from the user and user_id
        and  review_id context passed from
        ReplyViewSet
        """

        user_id=self.context['user_id']
        review_id=self.context['review_id']

        return (
            Reply.objects.create(
                user_id=user_id,
                review_id=review_id
                ,**validated_data
                )
            )




# !Simple Product
class SimpleProductSerializer(ModelSerializer):
    product_image=ProductImageSerializer(many=True)


    class Meta:
        model=Product
        fields=[
            'id',
            'title',
            'price',
            'product_image'
        ]




# ! Cart Item Serializer
class CartItemSerializer(ModelSerializer):
    product=SimpleProductSerializer()

    # * Custom field for finding total price of an item in cart
    total_product_price=(
        serializers.SerializerMethodField(
            method_name='get_product_price'
            )
        )


    def get_product_price(self,cart_item):
        """
        Custom Method for calculating cart item total
        price based on quantity and price of the product
        """
        return  cart_item.product.price * cart_item.quantity
    

    class Meta:
        model=CartItem
        fields=[
            'id',
            'product',
            'quantity',
            'total_product_price'
        ]



# !Cart Serializer 
class CartSerializer(ModelSerializer):
    class Meta:
        model=Cart 
        fields=[
            'id',
            'user',
            'time_stamp',

        ]


