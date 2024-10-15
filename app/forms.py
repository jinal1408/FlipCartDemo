from django import forms
from .models import Address,Product

class AddressForm(forms.ModelForm):
    class Meta:       
        model = Address
        fields = ['contactnum','addr','pincode']

class ProductRegister(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productid','productname','category','description','price','image']






