from .views import UserActvityViewSet

from django.urls import path 
from rest_framework_nested import routers



router=routers.DefaultRouter()
router.register('user',UserActvityViewSet,basename='user_profile')

urlpatterns = router.urls

