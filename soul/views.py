
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages 
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from .models import FoodItem , FoodOrderItem , FoodOrder , Coupon
from .forms import AddressForm , CouponForm
# Create your views here.
def index(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    return render(request , 'soul/index.html')
@login_required(login_url='login')
def ordernow(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    username = request.user.username
    all_food = FoodItem.objects.all()
    user_cart_items = request.user.cart.order_items.all()
    total = len(user_cart_items)
    context = {'somename' : username , 'all_food' : all_food , 'user_cart_items' : user_cart_items , 'total' : total}
    return render(request , 'soul/ordernow.html', context)

@login_required(login_url='login')
def cart(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    target_user = request.user
    target_cart = target_user.cart
    target_cart.check_do()
    all_foi = target_cart.order_items.all()
    total = len(all_foi)
    if total == 0 :
        return redirect('emptycart')
    return render(request , 'soul/cart.html' , {'somename' : request.user.username , 'all_foi' : all_foi , 'total' : total}  )

@login_required(login_url='login')
def add(request,**kwargs):
    storage = get_messages(request)
    for message in storage:
        temp = message
    main_key = kwargs['pk']
    target_user = request.user
    target_cart = target_user.cart
    all_foi = target_cart.order_items.all()
    done = False
    for foi in all_foi:
        temp_key = foi.item_type.pk
        if temp_key == main_key:
            done = True
            foi.item_quantity += 1
            foi.save()
            target_cart.save()
            break
    if done == False:
        the_dish = FoodItem.objects.get(pk = main_key)
        new_foi = FoodOrderItem(item_type=the_dish)
        new_foi.save()
        target_cart.order_items.add(new_foi)
        target_cart.save()
    return redirect('ordernow')

@login_required(login_url='login')
def remove(request,**kwargs):
    storage = get_messages(request)
    for message in storage:
        temp = message
    main_key = kwargs['pk']
    target_user = request.user
    target_cart = target_user.cart
    all_foi = target_cart.order_items.all()
    for foi in all_foi:
        temp_key = foi.item_type.pk
        if temp_key == main_key:
            if foi.item_quantity <= 1:
                target_cart.order_items.remove(foi)
                target_cart.save()
            else:
                foi.item_quantity -= 1
                foi.save()
            break
    
    return redirect('ordernow')

@login_required(login_url='login')
def discard(request,**kwargs):
    storage = get_messages(request)
    for message in storage:
        temp = message
    main_key = kwargs['pk']
    target_user = request.user
    target_cart = target_user.cart
    all_foi = target_cart.order_items.all()
    for foi in all_foi:
        temp_key = foi.item_type.pk

        if temp_key == main_key:

            target_cart.order_items.remove(foi)
            target_cart.save()
            
    
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    target_user = request.user
    target_cart = target_user.cart
    target_order_items = target_cart.order_items.all()
    if len(target_order_items) == 0:
        return redirect('emptycart')
    

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("ordernow")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,template_name = "soul/register.html",context={"form":form})

    form = UserCreationForm
    return render(request = request,template_name = "soul/register.html",context={"form":form})

def login_request(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.info(request, f"You are now logged in as {username}")
                return redirect('ordernow')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,template_name = "soul/login.html",context={"form":form})

def logout_request(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")

def emptycart(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    return render(request= request , template_name = 'soul/emptycart.html')

@login_required(login_url='login')
def address(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    useraddress = request.user.useraddress.address
    userpincode = request.user.useraddress.pincode
    context = {'useraddress' : useraddress , 'userpincode' : userpincode}
    return render(request= request  , template_name = 'soul/address.html' , context = context )

@login_required(login_url='login')
def updateaddress(request):
    target = request.user
    storage = get_messages(request)
    for message in storage:
        temp = message
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            target.useraddress.address = form.cleaned_data.get('address')
            target.useraddress.pincode = form.cleaned_data.get('pincode')
            target.useraddress.save()
            messages.success(request, "Address Updated !")
            return redirect('address')
        else:
            messages.error(request, "Invalid address or pincode")
    
    form = AddressForm()
    return render(request = request , template_name= 'soul/updateaddress.html' , context={'form' : form} )

@login_required(login_url='login')
def validate(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    if len(request.user.cart.order_items.all()) <= 0:
        return redirect('emptycart')
    return redirect('address')

@login_required(login_url='login')
def validate_coupon(request , **kwargs):
    storage = get_messages(request)
    for message in storage:
        temp = message
    coupon_code = kwargs['code']
    for coupon in Coupon.objects.all():
        if coupon.coupon_code == coupon_code:
            request.user.cart.discount_coupon = coupon
            request.user.cart.save()
            rkey =  request.user.cart.check_do()
            if rkey == 1:
                return redirect('couponsuccess')
            
            return redirect('couponfailure')

    return redirect('couponfailure')

@login_required(login_url='login')
def placeorder(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    target_user = request.user
    target_cart = target_user.cart
    all_foi = target_cart.order_items.all()
    new_order = FoodOrder(user = target_user)
    new_order.save()
    temp = request.user.cart.order_total()
    new_order.discount_applied = temp[1]
    new_order.save()
    for foi in all_foi:
        target_cart.order_items.remove(foi)
        new_order.order_items.add(foi)
    default_coupon = Coupon.objects.get(pk = 3)
    target_cart.discount_coupon = default_coupon
    target_cart.save()
    new_order.save()
    messages.success(request, "Order Placed !")
    return redirect('myorders')

@login_required(login_url='login')
def myorders(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    all_orders = FoodOrder.objects.filter(user = request.user).order_by('-order_time')
    username = request.user.username
    return render(request = request , template_name='soul/myorders.html' , context={'somename':username ,'all_orders' : all_orders})

@login_required(login_url='login')
def vieworder(request,**kwargs):
    storage = get_messages(request)
    for message in storage:
        temp = message
    main_key = kwargs['pk']
    order = FoodOrder.objects.get(pk = main_key)
    if order.user == request.user:
        return render(request = request , template_name= 'soul/vieworder.html' , context= {'order' :order})
    return redirect('myorders')

def couponsuccess(request):
    return render(request= request , template_name = 'soul/couponsuccess.html')

def couponfailure(request):
    return render(request= request , template_name = 'soul/couponfailure.html')

@login_required(login_url='login')
def applycoupon(request):
    storage = get_messages(request)
    for message in storage:
        temp = message
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            coupon_code = form.cleaned_data.get('coupon_code')
            for coupon in Coupon.objects.all():
                if coupon.coupon_code == coupon_code:
                    request.user.cart.discount_coupon = coupon
                    request.user.cart.save()
                    rkey =  request.user.cart.check_do()
                    if rkey == 1:
                        return redirect('couponsuccess')
                    
                    return redirect('couponfailure')

        return redirect('couponfailure')
            
    form = CouponForm()
    return render(request = request , template_name= 'soul/applycoupon.html' , context={'form' : form} )