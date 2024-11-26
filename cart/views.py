from django.shortcuts import render,redirect, get_object_or_404
from .models import Cart,CartItem,Order,OrderItem
from core.models import Fooditem,Customer,Category
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
import random

# Create your views here.
def cart_add(request, fooditem_id):
    fooditem = get_object_or_404(Fooditem, id=fooditem_id)
    cart, created = Cart.objects.get_or_create(customer=request.user, status='pending')

    cartitem, created = CartItem.objects.get_or_create(cart=cart, fooditem=fooditem)
    
    if not created:
        cartitem.quantity += 1
        cartitem.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
def cart(request):
    categories = Category.objects.all()
    cart, created = Cart.objects.get_or_create(customer=request.user, status='pending')
    cartitems = cart.cartitem_set.all()
    total_price = sum(
        item.quantity * (item.fooditem.off_price if item.fooditem.off_price else item.fooditem.price)for item in cartitems )    
    context = {'cart': cart, 'cartitems': cartitems, 'total_price':total_price, 'categories': categories}

    return render(request, 'cart/cart.html', context)
 


def cart_update(request, cartitem_id, quantity):
    cartitem = get_object_or_404(CartItem, id=cartitem_id, cart__customer=request.user, cart__status='pending')
    
    if quantity > 0:
        cartitem.quantity = quantity
        cartitem.save()
    else:
        cartitem.delete()  
    
    return redirect('cart') 

def cart_delete(request, cartitem_id):
    cartitem = get_object_or_404(CartItem, id=cartitem_id, cart__customer=request.user, cart__status='pending')
    cartitem.delete()
    
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    categories = Category.objects.all()
    cart, created = Cart.objects.get_or_create(customer=request.user, status='pending')
    cartitems = cart.cartitem_set.all()
    total_price = sum(
        item.quantity * (item.fooditem.off_price if item.fooditem.off_price else item.fooditem.price)for item in cartitems )    
    userprofile = Customer.objects.filter(id=request.user.id).first()
    context = {'cart': cart, 'cartitems': cartitems, 'total_price':total_price,'userprofile':userprofile, 'categories':categories}

    return render(request, 'cart/checkout.html', context)



@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':

        currentuser=Customer.objects.filter(id=request.user.id).first()

        if not currentuser.firstname :
            currentuser.firstname = request.POST.get('fname')
            currentuser.lastname = request.POST.get('lname')
            currentuser.phone_number = request.POST.get('order_number')
            currentuser.email = request.POST.get('order_email')
            currentuser.address = request.POST.get('order_address')
            currentuser.save()

        neworder = Order()
        neworder.customer = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.order_number = request.POST.get('order_number')
        neworder.order_email = request.POST.get('order_email')
        neworder.order_address = request.POST.get('order_address')
        neworder.state = request.POST.get('state')
        neworder.city = request.POST.get('city')

        cart = get_object_or_404(Cart, customer=request.user, status='pending')
        cartitems = cart.cartitem_set.all()

        neworder.order_total = sum(item.quantity * item.fooditem.price for item in cartitems)

        track_num = 'dishdash' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_number=track_num).exists():
            track_num = 'dishdash' + str(random.randint(1111111, 9999999))
        neworder.tracking_number = track_num

        neworder.save()
        request.session['current_order'] = neworder.id

        for item in cartitems:
            OrderItem.objects.create(
                order=neworder,
                fooditem=item.fooditem,
                quantity=item.quantity,
                price=item.fooditem.price
            )

        cart.status = 'completed'
        # cart.cartitem_set.all().delete()
        cart.save()

        messages.success(request, 'Your Order Has Been Placed')

        return redirect('payment')

    return redirect('cart')

@login_required(login_url='login')
def payment(request):
    categories = Category.objects.all()
    cart, created = Cart.objects.get_or_create(customer=request.user, status='pending')
    cartitems = cart.cartitem_set.all()
    userprofile = Customer.objects.filter(id=request.user.id).first()
   
    current_order_id = request.session.get('current_order')
    current_order = Order.objects.get(id=current_order_id)

    total_price = current_order.order_total

    context = {
        'cart': cart, 
        'cartitems': cartitems, 
        'total_price':total_price,
        'userprofile':userprofile, 
        'categories':categories,
        'current_order':current_order}

    if request.method == 'POST':
        payment_mode = request.POST.get('payment_mode')

        current_order.payment_mode = payment_mode
        current_order.save()

        del request.session['current_order']

        messages.success(request, 'Payment Successful')
        return redirect('index')
    
   
    return render(request, 'cart/payment.html', context)
