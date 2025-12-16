from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login
from . models import Customer

# Create your views here.

def show_account(request):
    if request.POST and 'register' in request.POST:
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            address=request.POST.get('address')
            #Creates user acccounts.
            user=User.objects.create(
                username=username,
                password=password,
                email=email
            )
            # create customer account

            Customer.objects.create(
                user=user,
                phone=phone,
                address=address
            )
            success_message="User Registered Successfully!"
            messages.success(request,success_message)
        except Exception as e:
            error_message="Duplicate Username or Invalid Credentials."
            messages.error(request,error_message)

    return render(request,'account.html',)