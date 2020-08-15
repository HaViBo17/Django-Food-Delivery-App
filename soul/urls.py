from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ordernow/',views.ordernow , name = 'ordernow'),
    path('register/',views.register , name = 'register'),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path('add/<int:pk>/' , views.add , name = "add"),
    path('remove/<int:pk>/' , views.remove , name = "remove"),
    path('discard/<int:pk>/' , views.discard , name = 'discard'),
    path('cart/' , views.cart , name = 'cart'),
    path('emptycart/' , views.emptycart , name='emptycart'),
    path('address/' , views.address , name = 'address'),
    path('updateaddress/' , views.updateaddress , name = 'updateaddress'),
    path('validate/' , views.validate , name= 'validate' ) ,
    path('placeorder/' , views.placeorder , name = 'placeorder'),
    path('myorders/' , views.myorders , name = 'myorders'),
    path('vieworder/<int:pk>/' , views.vieworder , name = 'vieworder'),
    path('applycoupon/' , views.applycoupon , name = 'applycoupon'),
    path('couponsuccess/' , views.couponsuccess , name = 'couponsuccess'),
    path('couponfailure/' , views.couponfailure , name = 'couponfailure'),
]