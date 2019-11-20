from django.urls import path
from .views import HomeView,seller_details,add_to_cart
app_name = 'core'

urlpatterns = [
	path('',HomeView.as_view(),name='home'),
	path('menu/<int:seller_id>/',seller_details,name='menu'),
	path('menu/add-to-cart/<slug>/')

	]