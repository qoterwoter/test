from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, OrderViewSet, SupportViewSet, OrderRatingViewSet, \
    FeedbackViewSet, order_detail, choose_driver, UserViewSet, CarViewSet, DriverViewSet, update_response, \
    DriverResponseViewSet, get_rating
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'supports', SupportViewSet)
router.register(r'order-rating', OrderRatingViewSet)
router.register(r'feedbacks', FeedbackViewSet)
router.register(r'users', UserViewSet)
router.register(r'car', CarViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'driver-responses', DriverResponseViewSet)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('order-rating/<int:order_id>/', OrderRatingViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('orderDetail/<int:order_id>/', order_detail, name='order_detail'),
    path('choose-driver/', choose_driver),
    path('update-response/<int:response_id>/', update_response),
    path('get-rating/<int:driver_id>/', get_rating),
    path('', include(router.urls)),
]