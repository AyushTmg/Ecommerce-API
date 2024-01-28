
from .models import (
    Collection,
    Product
)

from .serializers import (
    CollectionSerializer,
    ProductSerailizer
)


from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response



# !Collection ViewSet
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    

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
    queryset=Product.objects.all().select_related('collection')
    serializer_class=ProductSerailizer

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
        
        similar_products = Product.objects.exclude(id=instance.id).filter(collection=instance.collection)
        related_serializer = self.serializer_class(similar_products, many=True)

        data = {
            'product_details': serializer.data,
            'similar_products': related_serializer.data
        }

        return Response(data)


    
    


