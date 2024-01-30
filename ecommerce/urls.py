from .views import (
    CollectionViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ReviewViewSet,
    ReplyListCreateView,
    CartViewSet,
    CartItemViewSet
)

from django.urls import path 
from rest_framework_nested import routers



router=routers.DefaultRouter()
router.register('collections',CollectionViewSet)
router.register('products',ProductViewSet)
router.register('cart',CartViewSet)

product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('images',ProductImageViewSet,basename='product_image')
product_router.register('reviews',ReviewViewSet,basename='product_review')

cart_router=routers.NestedDefaultRouter(router,'cart',lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart_items')

urlpatterns = router.urls+product_router.urls+cart_router.urls

urlpatterns+=[
    path('products/<str:product_pk>/reviews/<str:review_pk>/replies/', ReplyListCreateView.as_view(), name='review_reply'),
]

