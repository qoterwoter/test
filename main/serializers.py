from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CarDocument, Car, Order, SupportRequest, OrderRating, Feedback


class CarDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDocument
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    car_document_id = CarDocumentSerializer()

    class Meta:
        model = Car
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'client': {'required': False},
        }


class OrderRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRating
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class SupportRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SupportRequest
        fields = ('id', 'user', 'status', 'title', 'description')


class FeedbackSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ('id', 'client', 'rating', 'comment', 'status', 'date')


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ('id', 'name', 'rating', 'car', 'user')

class DriverResponseSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ('id', 'client', 'rating', 'comment', 'status', 'date'

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'username', 'email', 'password', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.save()
        return user
