from .models import Seller, Customer, Order, Meal, OrderItem


def get_menu_items(self, restaurant):
    objects_qs = Meal.objects.filter(restaurant=restaurant)
    if objects_qs.exists():
        return objects_qs
    else:
        return False
