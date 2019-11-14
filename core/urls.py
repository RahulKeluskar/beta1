from django.urls import path
from .views import HomeView,SellerDetailView
app_name = 'core'

urlpatterns = [
	path('',HomeView.as_view(),name='home'),
	path('menu/<slug>/',SellerDetailView.as_view,name='menu')

	]