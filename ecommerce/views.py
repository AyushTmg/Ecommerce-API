
from .models import (
    Collection,
    Product,
    ProductImage,
    Review,
    Reply,
    Cart,
    CartItem
)

from .serializers import (
    CollectionSerializer,
    ProductSerailizer,
    ProductImageSerializer,
    ReviewSerailizer,
    ReplySerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer
)
from .filters import ProductFilter
from .pagination import Default


from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.permissions import  IsAuthenticated,IsAdminUser,AllowAny


from django_filters.rest_framework import DjangoFilterBackend






# !Collection ViewSet
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    http_method_names=['get','head','options','post','delete']
    pagination_class=Default 


    def get_permissions(self):
        """
        Permission for Collection ViewSet
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser]
        
    
    def retrieve(self, request, *args, **kwargs):
        """ 
        Overriding the default retrieve method to 
        filter the product by the collection
        """
        
        instance=self.get_object()
        serializer=self.serializer_class(instance)

        products=Product.objects.filter(collection=instance)
        product_serializer=ProductSerailizer(products,many=True)

        data={
            'collection':serializer.data,
            'products':product_serializer.data
        }

        return Response(data)




# !Product ViewSet
class ProductViewSet(ModelViewSet):
    queryset=(
        Product.objects.all()
        .select_related('collection')
        .prefetch_related('product_image')
    )
    serializer_class=ProductSerailizer
    http_method_names=['get','head','options','post','delete','patch']
    pagination_class=Default

   
    #* For Searching,Filtering and Ordering products
    filter_backends=[
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    # * For Using the Custom filter for Product
    filterset_class=ProductFilter

    #* For Specifying the fields for searching and ordering
    search_fields=['title','description']
    ordering_fields=['price']


    def get_permissions(self):
        """
        Permission for Product ViewSet
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]
    

    

    def get_serializer_context(self):
        """ 
        Passing the user_id as serializer context
        for creating Product object with the logged 
        in user
        """
        user_id=self.request.user.id
        return {'user_id':user_id}
    
    
    def retrieve(self, request, *args, **kwargs):
        """ 
        Customized the default retrieve method 
        for showing product detail with similar
        products listing
        """

        instance = self.get_object()
        serializer = self.serializer_class(instance)
        
        similar_products = (
            Product.objects
            .exclude(id=instance.id)
            .filter(collection=instance.collection)
            .select_related('collection')
            .prefetch_related('product_image')
        )
        related_serializer = self.serializer_class(similar_products, many=True)

        data = {
            'product_details': serializer.data,
            'similar_products': related_serializer.data
        }

        return Response(data)




# !ProductImage ViewSet
class ProductImageViewSet(ModelViewSet):
    serializer_class=  ProductImageSerializer
    http_method_names=['get','head','options','post']

    # ! Permission for Product Image ViewSet
    permission_classes=[IsAuthenticated]
    

    def get_queryset(self):
        """ 
        Over Riding the queryset for filter 
        the product images by the product id 
        present in the URL  parameter
        """
        product_id=self.kwargs['product_pk']
        return ProductImage.objects.filter(product_id=product_id)


    def get_serializer_context(self):
        """
        Passing the product_id as serializer context
        for creating product image instance
        """
        product_id=self.kwargs['product_pk']
        return {'product_id':product_id}
    



# ! Review ViewSet
class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerailizer
    http_method_names=['get','head','options','post','delete']
    pagination_class=Default


    #* For Ordering reviews   
    filter_backends=[OrderingFilter]

    #* For Specifying the fields for ordering
    ordering_fields=['time_stamp']


    def get_permissions(self):
        """
        Permission for Review ViewSet
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser]


    def get_queryset(self):
        """ 
        Over Riding the queryset for filtering 
        the review's by the product id 
        present in the URL  parameter
        """
        product_id=self.kwargs['product_pk']

        return (
            Review.objects
            .filter(product_id=product_id)
            .select_related('user')
        )
    

    def get_serializer_context(self):
        """
        Passing the product_id and user_id as 
        serializer context for creating product
        review instance
        """

        product_id=self.kwargs['product_pk']
        user_id=self.request.user.id

        return {
            'product_id':product_id,
            'user_id':user_id
            }

    


# ! Reply View 
class ReplyListCreateView(ListCreateAPIView):
    serializer_class=ReplySerializer

    #* For Ordering reviews reply 
    filter_backends=[OrderingFilter]

    #* For Specifying the fields for ordering
    ordering_fields=['time_stamp']


    def get_permissions(self):
        """
        Permission for Review ViewSet
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser]    


    def get_queryset(self):
        """ 
        Over Riding the queryset for filtering 
        the review reply's by the review id 
        present in the URL  parameter
        """
        review_id=self.kwargs['review_pk']

        return (
            Reply.objects
            .filter(review_id=review_id)
            .select_related('user')
        )
    

    def get_serializer_context(self):
        """
        Passing the review_id and user_id as 
        serializer context for creating product
        reply instance
        """

        review_id=self.kwargs['review_pk']
        user_id=self.request.user.id

        return {
            'review_id':review_id,
            'user_id':user_id
        }
    

    def list(self, request, *args, **kwargs):
        """
        Over Riding the list  method to add
        corresponding review to it's replies
        """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        review=Review.objects.get(id=self.kwargs['review_pk'])
        review_serailizer=ReviewSerailizer(review)
        serializer = self.get_serializer(queryset, many=True)

        data={
            'review':review_serailizer.data,
            'replies':serializer.data
        }

        return Response(data)
    



# ! Cart ViewSet
class CartViewSet(ModelViewSet):
    queryset=(
        Cart.objects.all()
        .prefetch_related(
            'cart_item',
            'cart_item__product',
            'cart_item__product__product_image'
            )
        )
    serializer_class=CartSerializer

    # ! Permissions for Cart ViewSet
    permission_classes=[IsAuthenticated]

    


# ! Cart Item Serializer 
class CartItemViewSet(ModelViewSet):
    http_method_names=['get','head','options','post','delete','put']

    # ! Permissions For CartItem ViewSet
    permission_classes=[IsAuthenticated]


    def get_queryset(self):
        """
        Over Riding the queryset for filtering the cart
        item by cart_id presented at URL parameter and 
        also using select_related and prefetch_related
        for optimization
        """
        cart_id=self.kwargs['cart_pk']

        return (
            CartItem.objects
            .filter(cart_id=cart_id)
            .select_related('product')
            .prefetch_related('product__product_image')
        )
    

    def get_serializer_class(self):
        """
        Over Rding the get_serializer class for using 
        different serializer for different methods 
        """
        if self.request.method in ['GET','HEAD','OPTIONS']:
            return CartItemSerializer
        
        elif self.request.method=='PUT':
            return UpdateCartItemSerializer
        
        return AddCartItemSerializer
    

    def get_serializer_context(self):
        """
        Passing the cart Id to the serializer 
        """
        cart_id=self.kwargs['cart_pk']
        return {'cart_id':cart_id}
    


     
    
    
