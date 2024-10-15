from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CustomManager(models.Manager):
    def cloths_list(self):
        return self.filter(category__exact='Cloths')
    def electronics_list(self):
        return self.filter(category__exact='Electronics')
    def home_list(self):
        return self.filter(category__exact='Home')
    def kitchen_list(self):
        return self.filter(category__exact='Kitchen')
    def fashion_list(self):
        return self.filter(category__exact='Fashion')
    def shoes_list(self):
        return self.filter(category__exact='Shoes')
    def shoes_list(self):
        return self.filter(category__exact='Shoes')
    def mobiles_list(self):
        return self.filter(category__exact='Mobiles')


class Product(models.Model):
    userid = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    productid = models.IntegerField(primary_key=True)
    productname = models.CharField(max_length=100)
    type=(
        ("Cloths","Cloths"),
        ("Electronics","Electronics"),
        ("Home","Home"),
        ("Kitchen","Kitchen"),
        ("Fashion","Fashion"),
        ("Shoes","Shoes"),
        ("Shoes","Shoes"),
        ("Mobiles","Mobiles")
        )
    category= models.CharField(max_length=50,choices=type)
    description=models.TextField()
    price=models.IntegerField()
    image=models.ImageField(upload_to='photos')
    objects = models.Manager()
    productmanager=CustomManager()


class Cart(models.Model):
    userid = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    qty = models.IntegerField(default=0)

class Orders(models.Model):
    orderid = models.IntegerField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    productid = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    qty=models.PositiveIntegerField(default=0)


class Address(models.Model):
    userid = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    contactnum=models.IntegerField()
    addr=models.TextField()
    pincode=models.IntegerField()

# payment block is an option Not necessary to require
class Payment(models.Model):
    receiptid = models.IntegerField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    orderid = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    productid = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    totalprice=models.FloatField()


