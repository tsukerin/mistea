from django.contrib import admin
from .models import TeaCategory, Subscription, Tea

class TeaCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(TeaCategory, TeaCategoryAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ('teas',)  # Добавляем возможность выбора чаев в подписке
admin.site.register(Subscription, SubscriptionAdmin)

class TeaAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Tea, TeaAdmin)
