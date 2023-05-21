from .models import CarDocument, Car, Driver, Order, Feedback, SupportRequest, OrderRating, DriverResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CarDocumentAdmin(admin.ModelAdmin):
    list_display = ('driver_license', 'world_license', 'registration', 'car_status', 'date_created')


admin.site.register(CarDocument, CarDocumentAdmin)


class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_photo_path', 'car_document_id')


admin.site.register(Car, CarAdmin)


class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'car_name')

    def car_name(self, obj):
        if obj.car is not None:
            return obj.car.name
        else:
            return ""


admin.site.register(Driver, DriverAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'from_location', 'id', 'to_location', 'departure_time', 'client', 'driver', 'men_amount',
        'children_amount', 'created_at', 'comment')


admin.site.register(Order, OrderAdmin)


class OrderRatingAdmin(admin.ModelAdmin):
    list_display = ('order', 'communication_rating', 'driver_rating', 'transport_rating')


admin.site.register(OrderRating, OrderRatingAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('client', 'rating', 'comment', 'status', 'date')


admin.site.register(Feedback, FeedbackAdmin)


class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'status')


admin.site.register(SupportRequest, SupportRequestAdmin)


class DriverResponseAdmin(admin.ModelAdmin):
    list_display = ('order', 'driver', 'price', 'created_at')


admin.site.register(DriverResponse, DriverResponseAdmin)