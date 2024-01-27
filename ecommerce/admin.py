from .models import (
    Collection,
    Product,
    ProductImage,
    Review,
    Reply,
    Order,
    OrderItem,
    Cart,
    CartItem,
)


from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse 


    
""" 
Collection Admin where we can also view how many product
are there in a particular collection and the products
"""
# !Collection Admin
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','title','product_count']
    search_fields=['title__istartswith']


    @admin.display(ordering='product_count')
    def product_count(self,collection):
        url=(
            reverse('admin:ecommerce_product_changelist')
            +"?"
            +urlencode({
                'collection__id':str(collection.id)
            }))
        return format_html(f'<a href="{url}" target="_blank">{collection.product_count} Products</a>')
    

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('product'))
      



#! Product Image inline 
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra=3



#! Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','title','unit_price','collection','is_available']
    search_fields=['title__istartswith']
    autocomplete_fields=['user','collection']
    inlines=[ProductImageInline]
    list_filter=['collection','user']


#! Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','product','description','user','time_stamp']
    search_fields=['description__istartswith']
    autocomplete_fields=['user','product']

    

# ! Reply Admin
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','review','description','user','time_stamp']
    autocomplete_fields=['user']



# ! Order Item Inline 
class OrderItemInline(admin.TabularInline):
    model=OrderItem
    extra=3
    autocomplete_fields=['product']



# ! Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','payment_status','user','time_stamp']
    autocomplete_fields=['user']
    inlines=[OrderItemInline]
    list_filter=['user']

    

# !Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id']
    search_fields=['user__istartswith']
    autocomplete_fields=['user']



# !Cart Item Admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','cart','quantity','product']
    autocomplete_fields=['product','cart']

    

