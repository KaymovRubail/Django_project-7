from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from product.models import Product,Category
from product.forms import ProductForm, CategoryForm,ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def hello_view(request):
    return HttpResponse("Hi, it is my project")
def current_date_view(request):
    return HttpResponse(f"{datetime.now()}")
def goodbye_view(request):
    return HttpResponse("Bye Bye")
def main_view(request):
    return render(request, 'index.html')
@login_required(login_url='/login/')
def products_view1(request,id):
    if request.method == 'GET':
        try:
            category = Category.objects.get(id=id)
            products = Product.objects.filter(category=category)
        except :
            return HttpResponse("page not found")
        return render(request=request,
                      template_name='product/product_list.html',
                      context={'products': products})
@login_required(login_url='/login/')
def products_view2(request):
    if request.method == 'GET':
        search=request.GET.get('search')
        page = request.GET.get('page',1)
        products=Product.objects.all()
        if search:
            # products=products.filter(title__icontains=search) | products.filter(content__icontains=search)
            products=products.filter(Q(title__icontains=search) | Q(content__icontains=search))
        limit=5
        maxp=products.count()/limit

        if maxp%1!=0:
            maxp=int(maxp)+1
        start= (int(page)-1)*limit
        end=start+limit
        products=products[start:end]


        return render(request=request,
                      template_name='product/product_list.html',
                      context={'products': products,'pages': range(1,maxp+1)})
@login_required(login_url='/login/')
def category_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, 'product/category_list.html', context={'c': categories})

@login_required(login_url='/login/')
def product__detail_view(request,id=0,prid=0):
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=prid)
        except Product.DoesNotExist:
            return HttpResponse("page not found")
        form = ReviewForm()
        return render(request=request,
                      template_name='product/product_deta