from django.shortcuts import render
from . models import product as Product
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    feutured_products=Product.objects.order_by('priority')[:4]
    latest_products=Product.objects.order_by('-id')[:4]
    context={
        'feutured_products':feutured_products,
        'latest_products':latest_products,
    }
    return render(request,'index.html',context)


def list_product(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    product_list=Product.objects.order_by('priority')
    paginator=Paginator(product_list,3)
    product_list=paginator.get_page(page)

    context={'products':product_list}
    return render(request,'products.html',context)
    
def detail_product(request,pk):
    product=Product.objects.get(pk=pk)
    context={'product':product}
    return render(request,'product_detail.html',context)
