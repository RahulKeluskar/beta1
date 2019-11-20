from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .helper_functions import (
    get_menu_items
)
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
    OrderItem
)


class HomeView(ListView):
    model = Seller
    paginate_by = 10
    template_name = "home.html"    


def seller_details(request,seller_id):
    seller = Seller.objects.get(pk=seller_id)
    context = dict()
    try:
        meals = Meal.objects.filter(restaurant_id=seller_id)
        print(meals)
        context = {
            'exists' : True,
            'meals' : meals,
            'seller' : seller
        }
        print(context)
        print("here")
        return render(request,"menu.html",context)
    except ObjectDoesNotExist:
        context={
            'exists' : False,
            'seller' : seller
        }
        print(context)
        return render(request,"menu.html",context)

def add_to_cart(request, slug):
	print("Hello")
	item = get_object_or_404(Meal, slug=slug) 
	order_item, created = OrderItem.objects.get_or_create(item=item,user=request.user, ordered = False)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]

		if order.items.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
		else:
			order.items.add(order_item)
			order_item.save()
	else:
		order = Order.objects.create(user=request.user, ordered_date= timezone.now())
		order.items.add(order_item) 
	return redirect("core:menu",slug=slug)
@login_required
def remove_from_cart(request,slug):
	print("Hello")
	item = get_object_or_404(Item,slug=slug)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		print("Hello2")
		order = order_qs[0]

		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
				item=item,
				user=request.user, 
				ordered=False
				)[0]
			order.items.remove(order_item)
		else:
			print("Hello3")
			return redirect("core:product", slug=slug)

			
	else:
		#add message saying user hasnt added to cart
		return redirect("core:product", slug=slug)
	return redirect("core:product",slug=slug)

@login_required
def remove_single_item_from_cart(request,slug):
	item = get_object_or_404(Item,slug=slug)
	order_qs = Order.objects.filter(
		user=request.user, 
		ordered=False
	)
	if order_qs.exists():
		order = order_qs[0]

		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(				item=item,
					user=request.user, 
					ordered=False
			)[0]
			order_item.quantity -= 1
			order_item.save()
			messages.info(request,"This items quantity was updated")
			return redirect("core:order-summary")
		else:
			return redirect("core:product", slug=slug)

			
	else:
		#add message saying user hasnt added to cart
		return redirect("core:product", slug=slug)
	return redirect("core:product",slug=slug)

@login_required
def add_single_item_to_cart(request,slug):
	item = get_object_or_404(Item,slug=slug)
	order_qs = Order.objects.filter(
		user=request.user, 
		ordered=False
	)
	if order_qs.exists():
		order = order_qs[0]

		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(item=item,
					user=request.user, 
					ordered=False
			)[0]
			order_item.quantity += 1
			order_item.save()
			messages.info(request,"This items quantity was updated")
			return redirect("core:order-summary")
		else:
			return redirect("core:product", slug=slug)

			
	else:
		#add message saying user hasnt added to cart
		return redirect("core:product", slug=slug)
	return redirect("core:product",slug=slug)
        


    