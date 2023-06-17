from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Car, Order, SupportRequest, OrderRating, Feedback, DriverResponse, Driver, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'username': {'required': False}, 'password': {'required': False}, 'phoneNumber': {'required': False}, 'is_staff': {'required': False}}

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            email=validated_data.get('email'),
            is_staff=validated_data.get('is_staff')
        )
        user.save()
        return user


class CarSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Car
        fields = '__all__'
        extra_kwargs = {'name': {'required': False}, 'car_photo_path': {'required': False}, 'car_pass': {'required': False}
            , 'photo_with_car_pass': {'required': False}, 'taxi_license': {'required': False}, 'car_status': {'required': False}}


class OrderRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRating
        fields = ('id', 'order', 'communication_rating', 'driver_rating', 'transport_rating')


class OrderSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()
    ratings = OrderRatingSerializer(required=False, read_only=True)
    client = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'ratings', 'from_location', 'to_location', 'departure_time', 'client',
                  'driver', 'men_amount', 'children_amount', 'created_at', 'comment', 'price', 'response', )
        extra_kwargs = {
            'client': {'required': False},
        }

    def get_response(self, obj):
        driver_response = DriverResponse.objects.filter(driver__user=self.context['request'].user, order=obj).first()
        if driver_response:
            serializer = DriverResponseSerializer(driver_response)
            return serializer.data
        else:
            return None


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
        model = Driver
        fields = ('id', 'rating', 'car', 'user')


class DriverResponseSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = DriverResponse
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'username', 'email', 'password', 'phoneNumber','is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            validated_data['phoneNumber'],
            validated_data['is_staff']
        )
        user.first_name = validated_data.get('first_name', '')
        user.last_name = validated_data.get('last_name', '')
        user.save()
        return user
