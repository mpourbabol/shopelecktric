from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail_view, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add_view, name='cart_add'),
    path('remove/<int:item_id>/', views.cart_remove_view, name='cart_remove'),
    path('update/<int:item_id>/', views.cart_update_view, name='cart_update'),
    path('coupon/', views.apply_coupon_view, name='apply_coupon'),
    path('compare/', views.compare_view, name='compare'),
    path('compare/add/<int:product_id>/', views.compare_add_view, name='compare_add'),
    path('compare/remove/<int:product_id>/', views.compare_remove_view, name='compare_remove'),
]
