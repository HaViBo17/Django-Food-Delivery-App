from django.db import models
from django.contrib.auth.models import  User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

# Create your models here.

class FoodItem(models.Model):
    item_name = models.CharField(max_length = 100)
    item_price = models.IntegerField(default = 100)
    item_rating = models.IntegerField(default = 5)
    item_image_url = models.CharField(max_length=1000)
    item_genre = models.IntegerField(default = 0)
    item_veg = models.IntegerField(default = 0)

    def __str__(self):
        return self.item_name

class FoodOrderItem(models.Model):
    item_quantity = models.IntegerField(default= 1)
    item_type = models.ForeignKey(FoodItem , default=1 , null = True , on_delete = models.CASCADE)
    def cost(self):
        return self.item_quantity * self.item_type.item_price

class Coupon(models.Model):
    min_order = models.IntegerField(default= 200)
    coupon_type = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    hard_discount = models.IntegerField(default=0)
    coupon_code = models.CharField(max_length=8 )

class FoodOrder(models.Model):
    user = models.ForeignKey(User , default= 1 , null = True , on_delete = models.SET_NULL)
    order_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    order_items = models.ManyToManyField(FoodOrderItem)
    discount_applied= models.DecimalField(max_digits= 10 , decimal_places= 2 , default= 0.00)
    def get_month(self):
        key = int(self.order_time.month)
        if key == 1:
            return 'Jan'
        if key == 2:
            return 'Feb'
        if key == 3:
            return 'Mar'
        if key == 4:
            return 'Apr'
        if key == 5:
            return 'May'
        if key == 6:
            return 'Jun'
        if key == 7:
            return 'Jul'
        if key == 8:
            return 'Aug'
        if key == 9:
            return 'Sep'
        if key == 10:
            return 'Oct'
        if key == 11:
            return 'Nov'
        if key == 12:
            return 'Dec'
        
    def order_total(self):
        total = 0.0
        for foi in self.order_items.all():
            total += foi.cost()
        

        tax = 0.05 * total

        gtotal = total + tax - float(self.discount_applied)
        return [total , float(self.discount_applied) , tax , gtotal]




class Cart(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE , primary_key=True)
    order_items = models.ManyToManyField(FoodOrderItem)
    discount_coupon = models.ForeignKey(Coupon , default= 3 ,null=True , on_delete = models.SET_DEFAULT)

    def check_do(self):
        total = 0
        for foi in self.order_items.all():
            total += foi.cost()
        if total < self.discount_coupon.min_order :
            default_coupon = Coupon.objects.get(pk = 3)
            self.discount_coupon = default_coupon
            self.save()
            return 0

        return 1


    def order_total(self):
        total = 0.0
        for foi in self.order_items.all():
            total += foi.cost()
        
        discount = 0
        if self.discount_coupon.pk != 3:
            if self.discount_coupon.coupon_type == 0:
                discount = self.discount_coupon.hard_discount
            else :
                discount = 0.01 * self.discount_coupon.percentage * total

        tax = 0.05 * total

        gtotal = total + tax - discount
        return [total , discount , tax , gtotal]
    
class Useraddress(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE , primary_key=True)
    address = models.CharField(max_length=1000 , default='Where do we deliver ? ')
    pincode = models.IntegerField(default=400076)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
        Useraddress.objects.create(user = instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.cart.save()