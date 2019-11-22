from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
from django_google_maps import fields as map_fields
from django.conf import settings

# Create your models here.


class Seller(models.Model):  # this is to create a new model for retaurant
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='restaurant')  # OneToOneField  is to ensure that one user have only one
    # restarant.
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='restaurant_logo/', blank=False)
    slug = models.SlugField(blank=True, null=True)
    geolocation = map_fields.GeoLocationField(
        max_length=100, blank=True, null=True)

    def __str__(self):
        return self.address

    def getimage(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url

    def get_absolute_url(self):
        return reverse("core:menu", kwargs={
            'id': self.id
        })


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=50, default="Customer")
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


# class Driver(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
#     avatar = models.CharField(max_length=500)
#     phone = models.CharField(max_length=500, blank=True)
#     address = models.CharField(max_length=500, blank=True)
#     location = models.CharField(max_length=500, blank=True)

#     def __str__(self):
#         return self.user.get_full_name()

class Meal(models.Model):
    restaurant = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='meal_images/', blank=False)
    price = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)

    def getimage(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def get_add_to_cart_url(self):
        return reverse(
            "core:add-to-cart",
            kwargs={
                'slug': self.slug
            }
        )

    def get_remove_from_cart_url(self):
        return reverse(
            "core:remove-from-cart",
            kwargs={
                'slug': self.slug
            }
        )

    def add_single_url(self):
        return reverse(
            "core:add-single-to-cart",
            kwargs={
                'slug': self.slug
            }
        )

    def remove_single_url(self):
        return reverse(
            "core:remove-single-from-cart",
            kwargs={
                'slug': self.slug
            }
        )

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    item = models.ForeignKey(Meal,
                             on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_final_price(self):
        return self.item.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(OrderItem)
    seller = models.ForeignKey(Seller,
                               on_delete=models.CASCADE, null=True)
    name = models.CharField(null=True, max_length=100)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
