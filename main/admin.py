from .models import CarDocument, Car, Driver, Order, Feedback, SupportRequest
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
    list_display = ('name', 'rating', 'car')


admin.site.register(Driver, DriverAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
    'from_location', 'to_location', 'departure_time', 'arrive_time', 'client', 'driver', 'order_status', 'men_amount',
    'children_amount', 'created_at', 'comment')


admin.site.register(Order, OrderAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('client', 'order', 'rating', 'comment')


admin.site.register(Feedback, FeedbackAdmin)


class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'status')


admin.site.register(SupportRequest, SupportRequestAdmin)
