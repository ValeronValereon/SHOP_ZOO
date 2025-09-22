from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from datetime import datetime

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # после регистрации — на страницу входа
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def index(request):
    products = Product.objects.all()
    return render(request, 'shop_zoo/index.html', {'products': products})

def single_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop_zoo/single_product.html', {'product': product})

def shop_zoo(request):
    products = Product.objects.all()
    return render(request, 'shop_zoo/product.html', {
        'products': products,
        'year': datetime.now().year
    })


     