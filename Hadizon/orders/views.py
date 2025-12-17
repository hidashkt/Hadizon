from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.decorators import login_required
from products.models import product as Product
# Create your views here.

@login_required(login_url="account")
def show_cart(request):
    user=request.user
    customer=user.customer_profile
    cart_obj,created=Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
       )
    context={'cart':cart_obj}
    return render(request,'cart.html')

@login_required(login_url="account")
def add_to_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=int(request.POST.get('quantity'))
        product_id=request.POST.get('product_id')
        cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        product=Product.objects.get(pk=product_id)
        ordered_item=OrderedItem.objects.create(
            product=product,
            owner=cart_obj,
            quantity=quantity,
        )
    return redirect('cart')