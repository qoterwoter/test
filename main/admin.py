from .models import Car, Driver, Order, Feedback, SupportRequest, OrderRating, DriverResponse
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_photo_path', 'car_pass', 'taxi_license', 'car_status')
    list_filter = ('car_status',)

    def approve_cars(self, request, queryset):
        queryset.update(car_status='approved')

    approve_cars.short_description = 'Установить статус "Одобрено"'

    def mark_as_moderating(self, request, queryset):
        queryset.update(car_status='moderating')

    mark_as_moderating.short_description = 'Установить статус "На модерации"'

    def moderate_cars(self, request, queryset):
        queryset.update(car_status='on_moderate')

    moderate_cars.short_description = 'Установить статус "Ожидает модерации"'

    actions = [approve_cars, moderate_cars, mark_as_moderating]


admin.site.register(Car, CarAdmin)


class DriverAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'rating', 'car_name', 'id')
    list_filter = ('rating',)

    def car_name(self, obj):
        if obj.car is not None:
            return obj.car.name
        else:
            return ""

    car_name.short_description = 'Машина'

    def user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    user_name.short_description = 'Имя водителя'


admin.site.register(Driver, DriverAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'from_location', 'id', 'to_location', 'departure_time', 'client', 'driver', 'men_amount',
        'children_amount', 'created_at', 'comment')
    list_filter = ('from_location', 'to_location')


admin.site.register(Order, OrderAdmin)


class OrderRatingAdmin(admin.ModelAdmin):
    list_display = ('order', 'communication_rating', 'driver_rating', 'transport_rating')


admin.site.register(OrderRating, OrderRatingAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('client', 'rating', 'comment', 'status', 'date')
    list_filter = ('status', 'client', 'rating')

    def make_published(self, request, queryset):
        queryset.update(status='publish')

    make_published.short_description = 'Установить статус "Опубликован"'

    def make_hiden(self, request, queryset):
        queryset.update(status='hiden')

    make_hiden.short_description = 'Установить статус "Скрыт"'

    def make_on_moder(self, request, queryset):
        queryset.update(status='on_moder')

    make_on_moder.short_description = 'Установить статус "На обработке"'

    actions = [make_published, make_hiden, make_on_moder]


admin.site.register(Feedback, FeedbackAdmin)


class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'status')
    list_filter = ('status', 'user')

    def mark_pending(self, request, queryset):
        queryset.update(status='pending')

    mark_pending.short_description = 'Установить статус "В ожидании"'

    def mark_ongoing(self, request, queryset):
        queryset.update(status='ongoing')

    mark_ongoing.short_description = 'Установить статус "В работе"'

    def mark_resolved(self, request: object, queryset: object) -> object:
        queryset.update(status='resolved')

    mark_resolved.short_description = 'Установить статус "Решен"'

    actions = [mark_pending, mark_ongoing, mark_resolved]


admin.site.register(SupportRequest, SupportRequestAdmin)


class DriverResponseAdmin(admin.ModelAdmin):
    list_display = ('display_order', 'display_driver', 'price', 'created_at', 'status', 'id')
    list_filter = ('status',)
    actions = ['select_driver', 'unselect_driver']

    def display_order(self, obj):
        return f"{obj.order.from_location} - {obj.order.to_location} ({obj.order.departure_time})"

    display_order.short_description = 'Заказ'

    def display_driver(self, obj):
        return f"{obj.driver.user.first_name} {obj.driver.user.last_name}"

    display_driver.short_description = 'Водитель'

    def select_driver(self, request, queryset):
        for driver_response in queryset:
            driver_response.status = 'a'
            driver_response.save()

    select_driver.short_description = 'Установить статус "Выбран пользователем"'

    def unselect_driver(self, request, queryset):
        for driver_response in queryset:
            driver_response.status = 'n'
            driver_response.save()

    unselect_driver.short_description = 'Сбросить статус'


admin.site.register(DriverResponse, DriverResponseAdmin)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active', 'phoneNumber', 'email', 'id')
    list_filter = ('is_staff', 'is_superuser', 'groups', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (('Персональная информация'), {'fields': ('phoneNumber', 'first_name', 'last_name',)}),
        (('Роли'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'phoneNumber', 'first_name', 'last_name', 'email', 'password1', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
