from django.contrib import admin
from .models import FoodItem , FoodOrder , Coupon
# Register your models here.
admin.site.register(FoodItem)
admin.site.register(FoodOrder)
admin.site.register(Coupon)