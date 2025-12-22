from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
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


def remove_item_from_cart(request,pk):
    item=OrderedItem.objects.get(pk=pk)
    if item:
       item.delete()
    
    return redirect('cart')

def checkout_cart(request):
    if request.POST:
      try:
        user=request.user
        customer=user.customer_profile
        total=float(request.POST.get('total'))
        order_obj = Order.objects.get(
        owner=customer,
        order_status=Order.CART_STAGE
        )
        if order_obj:
            order_obj.order_status=Order.ORDER_CONFIRMED
            order_obj.save()
            status_message="Your order is processed! Your item will be delivered within 5 days."
            messages.success(request,status_message)
        else:
            status_message="Unable to processed! No items in cart."
            messages.error(request,status_message)
      except Exception as e:
         status_message="Your order is processed! Your item will be delivered within 5 days."
         messages.error(request,status_message)
    return redirect('cart')

          
                

           
    
          




@login_required(login_url="account")
def add_to_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=int(request.POST.get('quantity'))
        product_id=request.POST.get('product_id')
        cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )
        cart_obj.quantity = quantity
        cart_obj.save()

    
        product=Product.objects.get(pk=product_id)
        ordered_item, created = OrderedItem.objects.get_or_create(
        product=product,
        owner=cart_obj,
        defaults={'quantity': quantity}
    )
        if created:
            ordered_item.quantity=quantity
            ordered_item.save()
        else:
            ordered_item.quantity=ordered_item.quantity+quantity
            ordered_item.save()
    return redirect('cart')