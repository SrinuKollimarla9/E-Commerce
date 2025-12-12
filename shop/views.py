from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .models import Category, Product, CartItem, Order, OrderItem
from .forms import StyledUserCreationForm



def index(request):
    categories = Category.objects.all()
    products = Product.objects.select_related('category').all()
    return render(request, 'shop/index.html', {
        'categories': categories,
        'products': products,
    })


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {
        'products': products
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {
        'product': product
    })


def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    return render(request, 'shop/cart.html', {
        'cart_items': products
    })



def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id not in cart:
        cart.append(product_id)

    request.session['cart'] = cart
    return redirect('shop:cart')



def checkout(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    total = sum(product.price for product in products)

    if request.method == 'POST' and products.exists():
        order = Order.objects.create(total_amount=total)

        for product in products:
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price
            )

        request.session['cart'] = []  # clear cart
        return redirect('shop:order_history')

    return render(request, 'shop/checkout.html', {
        'products': products,
        'total': total
    })


def order_history(request):
    orders = Order.objects.prefetch_related('items').order_by('-created_at')
    return render(request, 'shop/order_history.html', {
        'orders': orders
    })
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "shop/order_detail.html", {"order": order})



def signup_view(request):
    if request.method == 'POST':
        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:index')
    else:
        form = StyledUserCreationForm()

    return render(request, 'shop/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop:index')
    else:
        form = AuthenticationForm()

    return render(request, 'shop/login.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('shop:index')