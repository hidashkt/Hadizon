from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.decorators import login_required
from products.models import product as Product
# Create your views here.

@login_required(login_url="account")
def show_cart(request):
    customer = request.user.customer_profile

    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )

    cart_items = OrderedItem.objects.filter(owner=cart_obj)

    context = {
        'cart': cart_obj,
        'cart_items': cart_items
    }

    return render(request, 'cart.html', context)

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
        ordered_item=OrderedItem.objects.get_or_create(
            product=product,
            owner=cart_obj,
            quantity=quantity,
        )
        if created:
            ordered_item.quantity=quantity
            ordered_item.save()
        else:
            ordered_item.quantity=ordered_item.quantity+quantity
            ordered_item.save()
    return redirect('cart')