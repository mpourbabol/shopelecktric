from django.contrib import admin

from .models import Coupon, ItemOrder, Order


class ItemOrderInline(admin.TabularInline):
    model = ItemOrder
    extra = 0
    readonly_fields = ('product', 'variant', 'quantity', 'user')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active', 'start', 'end')
    list_filter = ('active',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'paid', 'discount', 'create')
    list_filter = ('paid', 'create')
    search_fields = ('email', 'f_name', 'l_name')
    inlines = [ItemOrderInline]


@admin.register(ItemOrder)
class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'variant', 'quantity', 'user')
