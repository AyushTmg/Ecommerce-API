from .models import (
    Collection,
    Product,
    ProductImage,
    Review,
    Reply,
    Cart,
    CartItem,
    Order,
    OrderItem
)
from .signals import order_created



from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,ValidationError


from django.db import transaction




# !Collection Serializer
class CollectionSerializer(ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title']




# !Product Image Serializer
class ProductImageSerializer(ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['id','image']
    
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
    upload_image=serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model=Product
        fields=[
            'id'
            ,'title'
            ,'description'
            ,'price'
            ,'is_available'
            ,'collection',
            'product_image',
            'upload_image'
            
        ]


    def create(self, validated_data):
        """ 
        Used for Creating a new product and its images
        with the validated data from the user and user_id
        context passed from ProductViewSet
        """
        uploaded_images=validated_data.pop('upload_image')
        print("This is the uploaded images ",uploaded_images)
        user_id=self.context['user_id']

        product=(
            Product.objects.create(
                user_id=user_id,
                **validated_data
                )
        )
        
        # ! For Creating the Product Images 
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product






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
                **validated_data
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




# ! Cart Item Serializer For View a Cart Item
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




# ! Add Cart Item Serailizer
class AddCartItemSerializer(ModelSerializer):
    product_id=serializers.IntegerField()
    
    class Meta:
        model=CartItem
        fields=['product_id','quantity']


    def validate_product_id(self,value):
        # ? Check if product id exists in Product Model
        if not Product.objects.filter(id=value).exists():
            raise ValidationError("Product with the given id doesn't exist")
        return value
        

    def save(self, **kwargs):
        """
        Over riding the save method to create 
        a new cart item instance or to update it  
        """
        cart_id=self.context['cart_id']
        user_id=self.context['user_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        
        # ! Check if cart with the cart_id exists or not 
        cart=Cart.objects.filter(id=cart_id,user_id=user_id).exists()
        if not cart:
            raise  ValidationError('No Such Cart with the given cart_id and User exists')

        # ! Expection is handeled here 
        try:
            # ! if cart item already exists then it just update the quantity
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity+=quantity
            cart_item.save()
    
        except Exception as e:
            # ! If there is no such cart item for this product new cart item is created
            cart_item=CartItem.objects.create(cart_id=cart_id,**self.validated_data)

        # ! At last returning the cart_item
        return cart_item

    


# ! Update Cart Item Serializer 
class UpdateCartItemSerializer(ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','quantity']



    
# !Cart Serializer 
class CartSerializer(ModelSerializer):
    cart_item=CartItemSerializer(many=True,read_only=True)

     # * Custom field for finding total price of cart incuding all cart items
    total_price=serializers.SerializerMethodField(method_name='get_total_price')


    def get_total_price(self,cart):
        """
        Calculate Total Price of a particular cart by
        summing up all prices of its items
        """
        total_price=sum(
                cart_item.product.price * cart_item.quantity 
                for cart_item in cart.cart_item.all()
            )

        return total_price


    class Meta:
        model=Cart 
        fields=[
            'id',
            'cart_item',
            'time_stamp',
            'total_price'

        ]

    def create(self, validated_data):
        user_id=self.context['user_id']
        return Cart.objects.create(
            user_id=user_id
        )




# !Order Item Serializer
class OrderItemSerailizer(ModelSerializer):
    product=SimpleProductSerializer()
    total_product_price=serializers.SerializerMethodField(method_name='get_total_product_price')

    def  get_total_product_price(self,order_item):
        """
        Custom Method for calculating specific order item total
        price based on quantity and price of the product
        """
        return  order_item.product.price*order_item.quantity
    
    class Meta:
        model=OrderItem
        fields=[
            'id',
            'product',
            'quantity',
            'total_product_price'
        ]




# ! Create Order Serailizer 
class CreateOrderSerailzer(serializers.Serializer):
    
    def validate(self,attrs):
        """
        Method for validating cart id 
        """
        user_id=self.context['user_id']
        cart=Cart.objects.get(user_id=user_id)
        if  not cart:
            raise ValidationError("Cart with given cart id user_id  doesnt exists")
        
        if CartItem.objects.filter(cart=cart).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        
        return attrs


    def save(self, **kwargs):
        """
        Method which get the user cart and 
        orders all the cart item in the cart 
        """
        with transaction.atomic():
            user_id=self.context['user_id']
            
            #! Get the cart object from db using validated data
            cart=Cart.objects.get(user_id=user_id)

            # ! Create new order with the user_id
            order=Order.objects.create(user_id=user_id)

            cart_items=CartItem.objects.filter(cart=cart)
            
            order_items=[
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,

                ) for item in cart_items
            ]
            
            # !Creating order items
            OrderItem.objects.bulk_create(order_items)

            # ! Deleteing a cart after the order adn order item is created
            cart.delete()

            # ! Creating another cart for the same user after deleting the ordered cart
            Cart.objects.create(user_id=user_id)

            #  ! Custome signal fired 
            order_created.send_robust(self.__class__,order=order)
            return order 




# ! Order Seriaizer For Viewing Orders 
class  OrderSerializer(ModelSerializer):
    user=serializers.StringRelatedField()
    order_item=OrderItemSerailizer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField('get_total_price')


    def get_total_price(self,order):
        """ 
        Custome serailizer field to calculate 
        the total order price including prices 
        of all order items 
        """
        total_price=sum(
            [item.product.price * item.quantity
            for item in order.order_item.all()]
        )
        return total_price

    
    class Meta:
        model=Order
        fields=[
            'id',
            'user',
            'payment_status',
            'order_item',
            'time_stamp',
            'total_price',
        ]




# ! Fo Updating Cart item Serailizer
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta :
        model=Order
        fields=['payment_status']




# ! Cancel Order Serializer
class CancelOrderSerializer(serializers.Serializer):
    pass
