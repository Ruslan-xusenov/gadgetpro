from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category
from .forms import ProductForm

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def add_product(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Sizda mahsulot qo‘shishga ruxsat yo‘q!")

    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('product_list')
    return render(request, 'products/add_product.html', {'form': form})


@login_required
def edit_product(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("Sizda mahsulotni tahrirlashga ruxsat yo‘q!")

    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'products/edit_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("Sizda mahsulotni o‘chirishga ruxsat yo‘q!")

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/delete_product.html', {'product': product})

def can_add_product(user):
    return user.groups.filter(name='ProductAdders').exists()

def is_product_adder(user):
    return user.groups.filter(name='ProductAdders').exists()

@login_required
@user_passes_test(can_add_product)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all().order_by('-id')  # yangi mahsulotlar birinchi bo‘lib chiqadi
    return render(request, 'products/product_list.html', {'products': products})


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            # Foydalanuvchining sessiyasiga saqlash
            cart = request.session.get('cart', {})
            cart[product_id] = cart.get(product_id, 0) + 1
            request.session['cart'] = cart
            return JsonResponse({'success': True, 'message': 'Mahsulot savatga qo‘shildi'})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Mahsulot topilmadi'})
    return JsonResponse({'success': False, 'message': 'Noto‘g‘ri so‘rov'})