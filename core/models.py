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
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True, null=True)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()


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
    slug = models.SlugField(blank=True,null=True)

    def getimage(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
   


    def __str__(self):
        return self.name


class OrderItem(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller,
    on_delete=models.CASCADE)
    item = models.ForeignKey(Meal,
    on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}' from {self.seller.name} by {self.customer.name}"

class Order(models.Model):
    pass