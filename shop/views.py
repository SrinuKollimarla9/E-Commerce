from decimal import Decimal
import base64
import os
from io import BytesIO
from django.core.mail import EmailMessage


from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.utils import ImageReader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.utils import timezone

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

from .models import Product, CartItem, Order, OrderItem
from .forms import StyledUserCreationForm
from .invoice import generate_invoice_pdf, send_invoice_email



LOGO_BASE64 = """
https://lh3.googleusercontent.com/rd-gg-dl/ABS2GSkHdjd-NPhAMJzIuWwKaryfKOiCVcpiwwoVNebHm3B9SOnsyn6dmiQMbRARP3A4NmgfIihYCYlGEmxfH8EuoIv6HN1BH69j_EScFUVFci-oma7ZrkokVK0pfeXYkb4kcAVJDKRPxA9MlXDEuhefAJ7nmZ-sIkw1DjsjckYf7dyjzcFlflpEHpKETwmIP2McVpnCnlCYzvcPQiJCa634a5hh7ShOBtg46HrLVLAZIHxetMdGeqwxosZ3J9hSLOpEO6joiVoPxBQvoY4o9Sgdv1lW3J2pVPXSU5xINC4sKIivIMpVVrcGhj0WPcTn8uvOf-DMwuWX5RCRRwPvYF_esxEF6yf2t3l4SDlSlaMg48RpirhtRWOCSAlBmedymgub9qghb3ItfpvWmxxG3Tyo_-4pnGJwxFPqPwMHeCZwlUWqrLMRJcmiT9iNc54-DTfYPFF1XUVVCzh6hOC3jXrevC9EjwJHEBeqAobs9u5UKUWb44dtBY-Cxmf0zBohqdXJm5NZYtNuqkS_dQIzgHiSXzV8eAFKHWkgELJt5BgJybS0HABkIUIML9XvHthcVi9EvLh4ql3rxOWrJZAQZAhtokeZAyrW5DgcDxFeYBmUSyhbpSW8FKtNHz-KaG6t5Gkm1dRZzFu_UV2HOzuL9OrffeIgEHsRL-J1q0j3Po-bdlWzvG8k33Yiq1r08J17SJLKrVXsq7UCP5aQ-D-cWKRkQx2-hU_HGRppoFDPf2Ht2smrKlarhrwd4RX1HWAOBUia9apXcjCsFIeqtwCyMILWEudiqu6WfJTB08cbndJMQJ537Ki5b6sFT3IyZU2MXZRMvT8YgCCLVDauhHeijRk2wuEA6Y62NBzUPJ7Ss2MB0mJIVAM0-X6sknlr_wqwhDQAg8fdQVtfUfGg3a8y7aBqmCsqaHuCyLqSrmn-tTRIiiaPB8rMoc6fOt3fwX6lupIQVzcEFgkQYPj156MRCXSo6-ckGFNxRP3SIuC1-jHY6JPo8-AqBo1SndRap3KHRy7fhfrrA7qJsTLMae5Y8uRR4bBS93HVR2ecVs0m1HHIPFczSu032us8vDAHaLuykLxkoRWu3ejhXFBgOClAl8C_ro8vQ8toKPoOYL6J7_yJ-HqFp7VcLF3yMJt5dJwFsI7vAwUu1zvOAufzaywHIJfptlkAgyKV_t4OhRcTU4qihfbC9F-FNUXYgWFvRaj0g4-LGnNciNJndVPeLX13qw_XzXtP-LwrhZAapMGBLmpAFnrdj3SORuUm1ukeO7LDHJUhQ7hXaaB1mmzVmxQEOSdHVEdyzlfY8XZ7wdJi2gD1VzeWNQteeJl6akqo5xT6eI2LgRfF6qMJtxlBqGj1gGX1Cbv_URiBZi3YPJwvZYu5=s1024-rj
"""

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        cart_item.quantity = qty
    else:
        cart_item.quantity += qty

    cart_item.save()
    return redirect('shop:cart')


def index(request):
    products = Product.objects.all()
    return render(request, "shop/index.html", {"products": products})



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


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = sum(item.subtotal() for item in cart_items)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()

    return render(request, 'shop/order_detail.html', {
        'order': order,
        'items': items
    })





def order_history(request):
    orders = Order.objects.prefetch_related('items').order_by('-created_at')
    return render(request, 'shop/order_history.html', {
        'orders': orders
    })

def signup_view(request):
    if request.method == 'POST':
        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop:login')  # ✅ safest
    else:
        form = StyledUserCreationForm()

    return render(request, 'shop/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)   # now works
            return redirect('shop:index')
    else:
        form = AuthenticationForm()

    return render(request, 'shop/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('shop:index')

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity = int(request.POST['quantity'])
    item.save()
    return redirect('shop:cart')

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('shop:cart')

    # ✅ STEP 1: Calculate total price FIRST
    total_price = Decimal('0.00')

    for item in cart_items:
        total_price += item.product.price * item.quantity

    # ✅ STEP 2: Create Order WITH total_price
    order = Order.objects.create(
        user=request.user,
        total_price=total_price
    )

    # ✅ STEP 3: Create OrderItems
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.product.price,
            quantity=item.quantity
        )

    # ✅ STEP 4: Clear cart
    cart_items.delete()

    # ✅ STEP 5: Generate invoice PDF
    pdf_bytes = generate_invoice_pdf(order)

    # ✅ STEP 6: Email invoice
    send_invoice_email(order, pdf_bytes)

    return redirect('shop:order_detail', order.id)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {
        'order': order
    })

@login_required
def download_invoice(request, order_id):
    # Fetch order safely
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Create HTTP response for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_Order_{order.id}.pdf"'

    # Create PDF canvas
    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # ---- LOGO ----
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 40, height - 80, width=120, height=50, preserveAspectRatio=True)

    # ---- COMPANY DETAILS ----
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, height - 50, "Art Gallery")
    c.setFont("Helvetica", 10)
    c.drawString(200, height - 65, "Hyderabad, India")
    c.drawString(200, height - 80, "Email: support@artgallery.com")

    # ---- ORDER INFO ----
    y = height - 130
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, f"Invoice for Order #{order.id}")

    c.setFont("Helvetica", 10)
    y -= 20
    c.drawString(40, y, f"Order Date: {order.created_at.strftime('%d %b %Y')}")
    y -= 15
    c.drawString(40, y, f"Status: {order.status}")

    # ---- ITEMS HEADER ----
    y -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Product")
    c.drawString(250, y, "Price")
    c.drawString(330, y, "Qty")
    c.drawString(400, y, "Total")

    # ---- ITEMS ----
    c.setFont("Helvetica", 10)
    y -= 15
    subtotal = Decimal("0.00")

    for item in order.items.all():
        line_total = item.price * item.quantity
        subtotal += line_total

        c.drawString(40, y, item.product.name)
        c.drawString(250, y, f"₹ {item.price}")
        c.drawString(330, y, str(item.quantity))
        c.drawString(400, y, f"₹ {line_total}")
        y -= 15

    # ---- TAX CALCULATION (NO MODEL FIELD REQUIRED) ----
    GST_RATE = Decimal("0.18")  # 18%
    gst_amount = (subtotal * GST_RATE).quantize(Decimal("0.01"))
    grand_total = subtotal + gst_amount

    # ---- TOTALS ----
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(330, y, "Subtotal:")
    c.drawString(400, y, f"₹ {subtotal}")

    y -= 15
    c.drawString(330, y, "GST (18%):")
    c.drawString(400, y, f"₹ {gst_amount}")

    y -= 15
    c.drawString(330, y, "Total Payable:")
    c.drawString(400, y, f"₹ {grand_total}")

    # ---- FOOTER ----
    y -= 40
    c.setFont("Helvetica", 9)
    c.drawString(40, y, "Thank you for shopping with Art Gallery!")

    # Finish PDF
    c.showPage()
    c.save()

    return response
