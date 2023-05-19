from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CarDocument, Car, Order


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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'username', 'email', 'password', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        user.save()
        return user
