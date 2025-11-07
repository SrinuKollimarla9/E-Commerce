from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from .models import Product, CartItem, Order, OrderItem
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.db import transaction

def index(request):
    products = Product.objects.all()[:12]
    return render(request, 'shop/index.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('shop:cart')

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum([it.subtotal() for it in items]) if items.exists() else 0
    return render(request, 'shop/cart.html', {'items': items, 'total': total})

@login_required
@transaction.atomic
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        return redirect('shop:cart')
    total = sum([it.subtotal() for it in items])
    order = Order.objects.create(user=request.user, total=total)
    for it in items:
        OrderItem.objects.create(order=order, product=it.product, quantity=it.quantity, price=it.product.price)
        # reduce stock
        it.product.stock = max(it.product.stock - it.quantity, 0)
        it.product.save()
    # clear cart
    items.delete()
    return render(request, 'shop/checkout.html', {'order': order})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:index')
    else:
        form = SignUpForm()
    return render(request, 'shop/signup.html', {'form': form})

@login_required
def order_history(request):
    orders = request.user.orders.all()
    return render(request, 'shop/order_history.html', {'orders': orders})
