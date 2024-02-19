from .views import (
    CollectionViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ReviewViewSet,
    ReplyViewSet,
    CartViewSet,
    CartItemViewSet,
    OrderViewSet
)

from django.urls import path 
from rest_framework_nested import routers



router=routers.DefaultRouter()
router.register('collections',CollectionViewSet)
router.register('products',ProductViewSet)
router.register('cart',CartViewSet,basename='cart')
router.register('order',OrderViewSet,basename='order')

product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('images',ProductImageViewSet,basename='product_image')
product_router.register('reviews',ReviewViewSet,basename='product_review')


review_router=routers.NestedDefaultRouter(product_router,'reviews',lookup='review')
review_router.register('replies',ReplyViewSet,basename="review_reply")


cart_router=routers.NestedDefaultRouter(router,'cart',lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart_items')


urlpatterns = router.urls+product_router.urls+cart_router.urls+review_router.urls




