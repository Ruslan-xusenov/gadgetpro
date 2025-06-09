from django.shortcuts import render, redirect
from .forms import OrderForm
from cart.cart import Cart
from .models import Order, OrderItem

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity']
                )
            cart.clear()
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'orders/checkout.html', {'form': form})


def order_view(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        quantity = int(request.POST.get("quantity", 1))
        
        if not product_name:
            return render(request, "order.html", {"message": "Savat bo’sh! Buyurtma berishdan oldin mahsulot qo’shing."})
        
        Order.objects.create(product_name=product_name, quantity=quantity)
        return render(request, "order.html", {"message": "Buyurtma qabul qilindi! Sizga qisqa muddat ichida qo‘ng‘iroq qilishadi."})

    return render(request, "order.html")