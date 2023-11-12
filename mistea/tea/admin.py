from django.contrib import admin
from .models import UserProfile, TeaCategory, Subscription, Tea, Review, Order, Payment


class TeaCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(TeaCategory, TeaCategoryAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ('teas',)  # Добавляем возможность выбора чаев в подписке
admin.site.register(Subscription, SubscriptionAdmin)

class TeaAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'stock', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Tea, TeaAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'address']
admin.site.register(UserProfile, UserProfileAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['tea', 'subscription', 'user', 'rating', 'date']
admin.site.register(Review, ReviewAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'tea', 'delivery_interval', 'tea_format', 'delivery_address', 'status', 'order_date', 'total_amount', 'payment_method', 'payment_status']
    list_filter = ['status', 'order_date', 'delivery_interval', 'tea_format', 'payment_method', 'payment_status']
admin.site.register(Order, OrderAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'amount', 'payment_date', 'payment_method', 'payment_status', 'recurring', 'recurring_interval']
    list_filter = ['payment_date', 'payment_method', 'payment_status', 'recurring', 'recurring_interval']
admin.site.register(Payment, PaymentAdmin)





