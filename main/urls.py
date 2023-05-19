from django.urls import path, include
from .views import UserRegistrationView, UserLoginView
from .views import OrderViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('', include(router.urls)),
]