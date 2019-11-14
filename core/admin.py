from django.contrib import admin
from .models import Seller,Customer,Meal,Order,OrderDetails
# Register your models here.
admin.site.register(Seller)
admin.site.register(Customer)
# admin.site.register(Driver)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderDetails)
