from rest_framework import generics, status, decorators
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, UserRegistrationSerializer, SupportRequestSerializer, OrderRatingSerializer, \
    FeedbackSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .models import Order, SupportRequest, OrderRating, Feedback, Driver
from .serializers import OrderSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

    def perform_create(self, serializer):
        client = self.request.user
        serializer.save(client=client)


class OrderRatingViewSet(viewsets.ModelViewSet):
    queryset = OrderRating.objects.all()
    serializer_class = OrderRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(order_id=self.request.data['order'])

    def get_queryset(self):
        user = self.request.user
        return OrderRating.objects.filter(order__client=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class SupportViewSet(viewsets.ModelViewSet):
    queryset = SupportRequest.objects.all()
    serializer_class = SupportRequestSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SupportRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.filter(Q(status='publish'))

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(client=user)


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    driver = order.driver
    car = None
    if driver is not None:
        car = driver.car

    data = {
        'order_id': order.id,
        'from_location': order.from_location,
        'to_location': order.to_location,
        'departure_time': order.departure_time,
        'client': order.client.username,
        'driver_name': driver.name if driver else None,
        'driver_rating': driver.rating if driver else None,
        'car_name': car.name if car else None,
        'car_photo_path': car.car_photo_path if car else None,
        'car_document_id': car.car_document_id.id if car else None,
        'men_amount': order.men_amount,
        'children_amount': order.children_amount,
        'created_at': order.created_at,
        'comment': order.comment,
    }

    return JsonResponse(data)


@api_view(['POST'])
def choose_driver(request):
    order_id = request.data.get('order_id')
    driver_id = request.data.get('driver_id')
    order = Order.objects.get(id=order_id)
    driver = Driver.objects.get(id=driver_id)
    order.driver = driver
    order.save()
    return Response({'success': True})


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = response.data
        token, created = Token.objects.get_or_create(user_id=user['id'])
        user['token'] = token.key
        return Response(user, status=status.HTTP_201_CREATED)


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_data = UserSerializer(user).data
        token, created = Token.objects.get_or_create(user=user)
        user_data['token'] = token.key

        return Response(user_data, status=status.HTTP_200_OK)
