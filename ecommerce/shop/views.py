from django.http import  JsonResponse
from django.shortcuts import redirect, render
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from django import template
from django.shortcuts import render
from .models import Cart,Order
from django.contrib.auth.decorators import login_required
 
 
def home(request):
  products=Product.objects.filter(trending=1)
  return render(request,"shop/index.html",{"products":products})
 
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
 
 
 
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"shop/cart.html",{"cart":cart})
  else:
    return redirect("/")
 
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
 
 
 
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
 
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")
 
 
def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"shop/login.html")
 
def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"shop/register.html",{'form':form})
 
 
def collections(request):
  catagory=Catagory.objects.filter(status=0)
  return render(request,"shop/collections.html",{"catagory":catagory})
 
def collectionsview(request,name):
  if(Catagory.objects.filter(name=name,status=0)):
      products=Product.objects.filter(catagory__name=name)
      return render(request,"shop/products/index.html",{"products":products,"catagory_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')
 
 
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"shop/products/product_details.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('collections')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('collections')
    


@login_required
def checkout(request):
    # Get cart items for the current user
    cart = Cart.objects.filter(user=request.user)
    
    # Calculate the total amount and total cost dynamically
    total_amount = 0
    cart_items = []
    for item in cart:
        # Dynamically calculate the total cost for each item
        total_cost = item.product.selling_price * item.product_qty
        total_amount += total_cost
        cart_items.append({
            'product': item.product,
            'product_qty': item.product_qty,
            'total_cost': total_cost
        })
    
    if request.method == 'POST':
        # Capture shipping details and create a new order
        order = Order(
            user=request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            phone_number=request.POST['phone_number'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode'],
            landmark=request.POST.get('landmark', ''),  # optional field
            total_amount=total_amount
        )
        order.save()

        # Clear the cart after successful checkout
        cart.delete()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_success')  # Redirect to an order success page
    
    return render(request, 'shop/checkout.html', {'cart': cart_items, 'total_amount': total_amount})

def order_success(request):
    return render(request, 'shop/order_success.html')