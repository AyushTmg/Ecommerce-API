
from .models import (
    Collection,
    Product,
    ProductImage,
    Review,
    Reply
)

from .serializers import (
    CollectionSerializer,
    ProductSerailizer,
    ProductImageSerializer,
    ReviewSerailizer,
    ReplySerializer
)


from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response



# !Collection ViewSet
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    http_method_names=['get','head','options','post','delete']
    

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




#! Reply ViewSet
class ReplyViewSet(ModelViewSet):
    serializer_class=ReplySerializer
    http_method_names=['get','head','options','post','delete']


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
    



    
     
    
    
