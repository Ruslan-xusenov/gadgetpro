from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.contrib import messages
from .cart import Cart
from .forms import CheckoutForm
from .models import CartItem, Order, OrderItem

@login_required(login_url='login')
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:view_cart')

@login_required(login_url='login')
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required(login_url='login')
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart:view_cart')

@login_required(login_url='login')
def checkout(request):
    cart = Cart(request)

    if not cart:
        messages.warning(request, "Savat bo‘sh! Buyurtma berishdan oldin mahsulot qo‘shing.")
        return redirect('cart:view_cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']

            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                total_price=cart.get_total_price(),
                is_paid=False
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            cart.clear()  # Savatni tozalash
            messages.success(request, "Buyurtma muvaffaqiyatli yuborildi.")
            return redirect('cart:order_success')
    else:
        form = CheckoutForm()

    return render(request, 'cart/checkout.html', {'form': form, 'cart': cart})

@login_required(login_url='login')
def view_cart(request):
    cart = Cart(request)
    if not cart:
        messages.info(request, "Savat bo‘sh.")
    return render(request, 'cart/cart_detail.html', {'cart': cart})