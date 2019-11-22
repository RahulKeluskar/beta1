
from django.shortcuts import render, redirect, get_object_or_404
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
from .forms import (
    MealForm,
    SellerForm
)


class HomeView(ListView):
    model = Seller
    paginate_by = 10
    template_name = "home.html"


def seller_details(request, seller_id):
    seller = Seller.objects.get(pk=seller_id)
    context = dict()
    try:
        meals = Meal.objects.filter(restaurant_id=seller_id)
        print(meals)
        context = {
            'exists': True,
            'meals': meals,
            'seller': seller
        }
        print(context)
        print("here")
        return render(request, "menu.html", context)
    except ObjectDoesNotExist:
        context = {
            'exists': False,
            'seller': seller
        }
        print(context)
        return render(request, "menu.html", context)


def get_seller_object(obj):
    return obj.restaurant_id


def add_to_cart(request, slug):
    print("Hello")
    item = get_object_or_404(Meal, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, customer=request.user)
    seller = Seller.objects.get(id=item.restaurant_id)
    order_qs = Order.objects.filter(
        user=request.user, seller=seller, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
            order_item.save()
    else:
        order = Order.objects.create(user=request.user, seller=seller)
        order.items.add(order_item)
    return redirect("core:menu", seller.id)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object': order}
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


def remove_from_cart(request, slug):
    item = get_object_or_404(Meal, slug=slug)
    seller = Seller.objects.get(id=item.restaurant_id)
    order_qs = Order.objects.filter(
        user=request.user, seller=seller, ordered=False)
    if order_qs.exists():
        print("Hello2")
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user
            )[0]

            order.items.remove(order_item)
        else:
            print("Hello3")
            return redirect("core:menu", seller.id)
    else:
        messages.error(
            self.request, "This item has not been addded to cart yet")
        return redirect("core:menu", seller.id)
    return redirect("core:menu", seller.id)


def add_single_to_cart(request, slug):
    item = get_object_or_404(Meal, slug=slug)
    seller = Seller.objects.get(id=item.restaurant_id)
    order_qs = Order.objects.filter(
        user=request.user,
        seller=seller,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user
            )[0]
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "Quantity updated successfully")
            return redirect("core:view-cart")
        else:
            messages.error(request, "No order found for this item")
            return redirect("core:menu", id=seller.id)
    else:
        messages.error(request, "This item wasnt added to cart")
        return redirect("core:menu", id=seller.id)
    return redirect("core:home")


def remove_single_from_cart(request, slug):
    item = get_object_or_404(Meal, slug=slug)
    seller = Seller.objects.get(id=item.restaurant_id)
    order_qs = Order.objects.filter(
        user=request.user,
        seller=seller,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user
            )[0]
            order_item.quantity -= 1
            order_item.save()
            messages.success(request, "Quantity updated successfully")
            return redirect("core:view-cart")
        else:
            messages.error(request, "No order found for this item")
            return redirect("core:menu", seller.id)
    else:
        messages.error(request, "This item wasnt added to cart")
        return redirect("core:menu", seller.id)
    return redirect("core:home")


def add_meal(request):
    form = MealForm()

    if request.method == "POST":
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.restaurant = request.user.restaurant
            meal.slug = meal.restaurant.name+"_"+str(meal.id)
            meal.save()
            seller = Seller.objects.get(user=request.user)
            return redirect("core:menu", seller.id)
    return render(request, 'add-meal.html', {
        "form": form
    })


def add_seller(request):

    form = SellerForm

    if request.method == "POST":
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.slug = seller.name + "_" + str(request.user.id)
            seller.save()
            return redirect("core:menu", seller.id)
    return render(request, 'add-seller.html', {
        "form": form
    })
