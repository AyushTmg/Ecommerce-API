from .views import (
    CollectionViewSet,
    ProductViewSet,
)


from rest_framework_nested import routers



router=routers.DefaultRouter()
router.register('collections',CollectionViewSet)
router.register('products',ProductViewSet)


urlpatterns = router.urls
