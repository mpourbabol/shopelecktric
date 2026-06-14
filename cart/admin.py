from django.contrib import admin

from .models import Cart, Compare


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'variant', 'quantity')
    list_filter = ('user',)


@admin.register(Compare)
class CompareAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'session_key')
