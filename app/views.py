from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Cart,Orders,Address,Payment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView

# Create your views here.


def index(req):
    allproducts=Product.objects.all()
    context={'allproducts':allproducts}
    return render(req,'index.html',context)

# crude operations 
class ProductRegister(CreateView):
    model = Product
    fields="__all__"
    success_url="/"
    
# class ProductList(ListView):
#     model = Product
def ProductList(req):
    if req.user.is_authenticated:
        user=req.user
        object_list=Product.objects.filter(userid=user)
        context={'object_list':object_list,'username':user}
        return render(req,'app/product_list.html',context)


class ProductUpdate(UpdateView):
    model = Product
    template_name_suffix="_update_form"
    fields="__all__"
    success_url="/ProductList"

class ProductDelete(DeleteView):
    model = Product
    success_url="/ProductList"

def signup(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}

        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signup.html", context)
        elif upass != ucpass:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(req, "signup.html", context)
        else:
            try:
                userdata = User.objects.create(username=uname, password=upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("/signin")
            except:
                context["errmsg"] = "User Already exists"
                return render(req, "signup.html", context)
    else:
        context = {}
        context["errmsg"] = ""
        return render(req, "signup.html", context)


def signin(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" or upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signin.html", context)
        else:
            try:
                userdata = authenticate(username=uname, password=upass)
                if userdata is not None:
                    login(req, userdata)
                    return redirect("/")
                else:
                    context["errmsg"] = "Invalid username and password"
                    return render(req, "signin.html", context)
            except:
                context["errmsg"] = "User doesn't found"
                return render(req, "signin.html", context)
    else:
        return render(req, "signin.html")


def userlogout(req):
    logout(req)
    return redirect("/")


def fashionlist(req):
    allproducts=Product.productmanager.fashion_list()
    context={'allproducts':allproducts}
    return render(req,"index.html",context)


def clothslist(req):
    allproducts=Product.productmanager.cloths_list()
    context={'allproducts':allproducts}
    return render(req,"index.html",context)

def electronicslist(req):
    allproducts=Product.productmanager.electronics_list()
    context={'allproducts':allproducts}
    return render(req,"index.html",context)

def homelist(req):
    allproducts=Product.productmanager.home_list()
    context={'allproducts':allproducts}
    return render(req,"index.html",context)

def kitchenlist(req):
    allproducts=Product.productmanager.kitchen_list()
    context={'allproducts':allproducts}
    return render(req,"index.html",context)

def shoeslist(req):
    allproducts=Product.productmanager.shoes_list()
    context={'allproducts':allproducts}
    return render(req,"index.html",context)

def shoeslist(req):
    allproducts=Product.productmanager.shoes_list()
    context={'allproducts':allproducts}
    return render(req,"index.html",context)

def mobileslist(req):
    allproducts=Product.productmanager.mobiles_list()
    context={'allproducts':allproducts}
    return render(req,"index.html",context)



from django.db.models import Q

def searchproduct(req):
    query=req.GET.get('q')
    errmsg=""
    if query:
        allproducts=Product.objects.filter(
            Q(productname__icontains=query)
            |Q(category__icontains=query)
            |Q(description__icontains=query)
        )
        if len(allproducts)==0:
            errmsg="No product found!"
    else:
        allproducts=Product.objects.all()

    context={'allproducts':allproducts,'errmsg':errmsg}
    return render(req,'index.html',context)


def showpricerange(req):
    if req.method=='GET':
        return render(req,'index.html')
    else:
        r1=req.POST['min']
        r2=req.POST['max']
        if r1 is not None and r2 is not None and r1.isdigit() and r2.isdigit():
            allproducts=Product.objects.filter(price__range=(r1,r2))
            context={'allproducts':allproducts}
            return render(req,'index.html',context)
        else:
            allproducts=Product.objects.all()
            context={'allproducts':allproducts}
            return render(req,'index.html',context)


def sortingbyprice(req):
    sortoption=req.GET['sort']
    if sortoption=='low_to_high':
        allproducts=Product.objects.order_by('price')  #ASC Order
    elif sortoption=='high_to_low':
        allproducts=Product.objects.order_by('-price')  #DESC Order
    else:
        allproducts=Product.objects.all()

    context={'allproducts':allproducts}
    return render(req,'index.html',context)


def showcarts(req):
    user=req.user
    allcarts=Cart.objects.filter(userid=user.id)
    totalamount=0
    for x in allcarts:
        totalamount+=x.productid.price*x.qty
    totalitems=len(allcarts)

    if req.user.is_authenticated:
        context={'allcarts':allcarts,'username':user,'totalamount':totalamount,'totalitems':totalitems}
    else:
        context={'allcarts':allcarts,'totalamount':totalamount,'totalitems':totalitems}
    return render(req,'showcarts.html',context)


def addtocart(req,productid):
    if req.user.is_authenticated:
        user=req.user
    else:
        user=None

    allproducts=get_object_or_404(Product,productid=productid)
    cartitem,created=Cart.objects.get_or_create(productid=allproducts,userid=user)
    if not created:
        cartitem.qty+=1
    else:
        cartitem.qty=1
    cartitem.save()
    return redirect('/showcarts')


def removecart(req,productid):
    user=req.user
    cartitem=Cart.objects.get(productid=productid,userid=user.id)
    cartitem.delete()
    return redirect('/showcarts')

def updateqty(req,qv,productid):
    allcarts=Cart.objects.filter(productid=productid)
    if qv==1:
        total=allcarts[0].qty+1
        allcarts.update(qty=total)
    else:
        if allcarts[0].qty>1:
            total=allcarts[0].qty-1
            allcarts.update(qty=total)
        else:
            allcarts=Cart.objects.filter(productid=productid)
            allcarts.delete()
    return redirect('/showcarts')


from .forms import AddressForm
def addaddress(req):
    if req.user.is_authenticated:
        if req.method=="POST":
            form=AddressForm(req.POST)
            if form.is_valid():
                address=form.save(commit=False)   #commit=False means it will be editable 
                address.userid=req.user
                address.save()
                return redirect('/showaddress')
        else:
            form=AddressForm()

        context={'form':form}
        return render(req,'addaddress.html',context)
    else:
        return redirect('/signin')
   
def showaddress(req):
    if req.user.is_authenticated:
        addresses=Address.objects.filter(userid=req.user)
        if req.method=="POST":
            return redirect('//make_payment')
        context={'addresses':addresses}
        return render(req,'showaddress.html',context)
    else:
        return redirect('/signin')

import razorpay
import random


def make_payment(req):
    if req.user.is_authenticated:
        cart_items = Cart.objects.filter(userid=req.user.id)
        total_amount = sum(item.productid.price * item.qty for item in cart_items)
        user = req.user
        client = razorpay.Client(
            auth=("rzp_test_wH0ggQnd7iT3nB", "eZseshY3oSsz2fcHZkTiSlCm")
        )
        try:
            data = {
                "amount": int(total_amount * 100),
                "currency": "INR",
                "receipt": str(random.randrange(1000, 90000)),
            }
            payment = client.order.create(data=data)

            for item in cart_items:
                order_id = random.randrange(1000, 90000)
                orderdata = Orders.objects.create(
                    orderid=order_id,
                    productid=item.productid,
                    userid=user,
                    qty=item.qty,
                )

                orderdata.save()
                Payment.objects.create(
                    receiptid=order_id,
                    orderid=orderdata,
                    userid=user,
                    productid=item.productid,
                    totalprice=item.qty * item.productid.price,
                )
            cart_items.delete()
            context = {"data": payment, "amount": total_amount}
            return render(req, "make_payment.html", context)
        except:
            context = {}
            # context["errmsg"] = (
            #     "An error occurred while creating payment order. Please try again"
            # )
            return render(req, "make_payment.html", context)
    else:
        return redirect("/signin")











