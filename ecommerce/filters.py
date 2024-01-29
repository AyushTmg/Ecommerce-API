from .models import Product
from django_filters.rest_framework import FilterSet

class ProductFilter(FilterSet):
    """ 
    Custom Filter For Product For Advance
    Product Filtering 
    """
    class Meta:
        model=Product
        fields={
        'collection_id':['exact'],
        'price':['gt','lt'],
        'title': ['icontains'], 
        'description': ['icontains'],
        'is_available': ['exact'],
    }
        
