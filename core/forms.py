from django import forms
from django.contrib.auth.models import User
from .models import (
    Meal,
    Seller
)


class MealForm(forms.ModelForm):
    """ Docstring for meal """
    class Meta:
        model = Meal
        exclude = ("restaurant", "slug")


class SellerForm(forms.ModelForm):
    """ Docstring for seller """

    class Meta:
        model = Seller
        exclude = ("user", "slug", "geolocation")
