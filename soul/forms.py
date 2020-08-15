from django import forms

class AddressForm(forms.Form):
    address = forms.CharField(label='address', max_length=1000)
    pincode = forms.IntegerField(label = 'pincode' )

class CouponForm(forms.Form):
    coupon_code = forms.CharField(label='coupon_code' , max_length=8)