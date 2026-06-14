from django.contrib import admin

from .models import (
    Brand, Category, Chart, Color, Comment, Images, Product, Size, Variants, Views,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sub_cat', 'sub_category', 'create')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'brand', 'unit_price', 'discount', 'amount', 'available', 'sell', 'num_view',
    )
    list_filter = ('available', 'status', 'brand')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('category', 'color', 'size', 'favourite', 'like', 'unlike')


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'product')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rate', 'create', 'is_reply')
    list_filter = ('rate', 'is_reply')


@admin.register(Variants)
class VariantsAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_variant', 'unit_price', 'discount', 'amount')


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'variant', 'unit_price', 'update')


@admin.register(Views)
class ViewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'ip', 'create')
