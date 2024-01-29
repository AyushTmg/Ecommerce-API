from .views import (
    CollectionViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ReviewViewSet,
    ReplyViewSet,
)

from django.urls import path 
from rest_framework_nested import routers



router=routers.DefaultRouter()
router.register('collections',CollectionViewSet)
router.register('products',ProductViewSet)

product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('images',ProductImageViewSet,basename='product_image')
product_router.register('reviews',ReviewViewSet,basename='product_review')

reply_router=routers.NestedDefaultRouter(product_router,'reviews',lookup='review')
reply_router.register('replies',ReplyViewSet,basename='review_reply')




urlpatterns = router.urls+product_router.urls+reply_router.urls


