from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('payment/<int:order_id>/paid/', views.mark_paid_view, name='mark_paid'),
    path('payment/<int:order_id>/zarinpal/', views.zarinpal_stub_view, name='zarinpal_stub'),
    path('payment/callback/', views.payment_callback_view, name='payment_callback'),
    path('<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('', views.order_list_view, name='order_list'),
]
