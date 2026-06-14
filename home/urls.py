from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('search/', views.search_view, name='search'),
    path('favourite/<int:pk>/', views.favourite_toggle_view, name='favourite_toggle'),
]
