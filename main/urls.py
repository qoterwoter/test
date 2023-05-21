from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, OrderViewSet, SupportViewSet, OrderRatingViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'supports', SupportViewSet)
router.register(r'order-rating', OrderRatingViewSet)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('order-rating/<int:order_id>/', OrderRatingViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('', include(router.urls)),
]