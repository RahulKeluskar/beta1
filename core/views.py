from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.shortcuts import (
	render,
	redirect,
	get_object_or_404
	)
from .models import (
	Seller,
	Customer,
	Meal,
	Order,
	OrderDetails
	)

class HomeView(ListView):
	model = Seller
	paginate_by = 10
	template_name = "home.html"

class SellerDetailView(DetailView):
	model = Seller
	template_name = "menu.html"	
