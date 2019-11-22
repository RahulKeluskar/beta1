from django.urls import path
from .views import (
    HomeView,
    seller_details,
    add_to_cart,
    OrderSummaryView,
    remove_from_cart,
    add_single_to_cart,
    remove_single_from_cart,
    add_meal,
    add_seller
)
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('menu/<int:seller_id>/', seller_details, name='menu'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('view-cart/', OrderSummaryView.as_view(), name='view-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/',
         remove_single_from_cart, name='remove-single-from-cart'),
    path('add-single-to-cart/<slug>/',
         add_single_to_cart, name='add-single-to-cart'),
    path('seller/add-meal/', add_meal, name="add-meal"),
    path('add-seller/', add_seller, name="add-seller")

]
