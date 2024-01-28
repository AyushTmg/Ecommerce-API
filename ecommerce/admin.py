
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
Admins can also view how many product
are there in a particular collection and
also view thier detail with one click onthe number of product present
"""
# !Collection Admin
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','title','product_count']
    search_fields=['title__istartswith']


    @admin.display(ordering='product_count')
    def product_count(self,collection):
        """
        Returns the total number of product in a particular 
        collection with a link so when clicked it redirect
        to the those product of collection in admin page
        """
        url=(
            reverse('admin:ecommerce_product_changelist')
            +"?"
            +urlencode({
                'collection__id':str(collection.id)
            })
        )
        return format_html(f'<a href="{url}" target="_blank">{collection.product_count} Products</a>')
    

    def get_queryset(self, request):
        """ 
        Annotate the product_count with
        number of product in the particular
        collection
        """
        return (
            super()
            .get_queryset(request)
            .annotate(
                product_count=Count('product')
            )
        )
      

#! Product Image inline 
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra=3


""" 
Admins can view number of review's in a product
and no of order of a particular product with Product
Image as Inline and can view the detail by clicking
on the number of review or order of a product
"""
#! Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','title','price','collection','is_available','total_order_item','total_review']
    search_fields=['title__istartswith']
    autocomplete_fields=['user','collection']
    inlines=[ProductImageInline]
    list_filter=['collection','user']


    @admin.display(ordering='order_count')
    def total_order_item(self,product):
        """
        Returns the total number of orders to the product
        with a link so when clicked it redirect to the 
        those order of product in admin page
        """
        url=(
            reverse('admin:ecommerce_orderitem_changelist')
            +"?"
            +urlencode({
                'product__id':str(product.id)
            })
        )
        return format_html(f'<a href="{url}" target="_blank">{product.order_count} Order</a>')
    

    @admin.display(ordering='review_count')
    def total_review(self,product):
        """
        Returns the total number of review to the product
        with a link so when clicked it redirect to the 
        those review of product in admin page
        """
        url=(
            reverse('admin:ecommerce_review_changelist')
            +"?"
            +urlencode({
                'product__id':str(product.id)
            })
        )
        return format_html(f'<a href="{url}" target="_blank">{product.review_count} Review</a>')
    
    

    def get_queryset(self, request):
        """ 
        Annotate the order_count and review_count
        with number of order and review in the
        particular product
        """
        return (
            super()
            .get_queryset(request)
            .annotate(
                order_count=Count('order_item'),
                review_count=Count('review')
            )
        )


"""
Admins can also view how many replies
have a particular review got and can 
view them by clicking on the number 
"""
#! Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','product','description','user','time_stamp','total_replies']
    search_fields=['description__istartswith']
    autocomplete_fields=['user','product']
    list_filter=['user','product']


    @admin.display(ordering='reply_count')
    def total_replies(self,review):
        """
        Returns the total number of replies to this review
        with a link so when clicked it redirect to the 
        those replies in admin page
        """
        url=(
            reverse('admin:ecommerce_reply_changelist')
            +"?"
            +urlencode({
                'review__id':str(review.id)
            })
        )
        return format_html(f'<a href="{url}" target="_blank">{review.reply_count} Replies</a>')
        

    def get_queryset(self, request):
        """ 
        Annotate the reply_count with number of 
        reply in the particular review
        """
        return (
            super().get_queryset(request)
            .annotate(
                reply_count=Count('reply')
            )
        )
    

# ! Reply Admin
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','review','description','user','time_stamp']
    autocomplete_fields=['user','review']
    list_filter=['user','review']


# ! Order Item Inline 
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['product','quantity']
    list_filter=['product']
    autocomplete_fields=['product']


# ! Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id','payment_status','user','time_stamp']
    autocomplete_fields=['user']
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




    

