from django.urls import path
from .views import HomeView,seller_details
app_name = 'core'

urlpatterns = [
	path('',HomeView.as_view(),name='home'),
	path('menu/<int:seller_id>/',seller_details,name='menu')

	]