from django.contrib import admin
from .models import Product,Cart,Orders,Payment,Address

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "userid",
        "productname",
        "productid",
        "category",
        "description",
        "price",
        "image"
    ]

class CartAdmin(admin.ModelAdmin):
    list_display = [
        "userid",
        "productid",
        "qty",
    ]

class OrdersAdmin(admin.ModelAdmin):
    list_display = [
        "userid",
        "productid",
        "qty",
        "orderid",
    ]

class AddressAdmin(admin.ModelAdmin):
    list_display=[
        'userid',
        'contactnum',
        'addr',
        'pincode'
    ]

class PaymentAdmin(admin.ModelAdmin):
    list_display=[
        'receiptid',
        'userid',
        'orderid',
        'productid',
        'totalprice'
    ]

admin.site.register(Product,ProductAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Orders,OrdersAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Payment,PaymentAdmin)









