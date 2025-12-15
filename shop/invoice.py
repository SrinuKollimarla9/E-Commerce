from io import BytesIO
from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMessage

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_invoice_pdf(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ===== HEADER =====
    p.setFont("Helvetica-Bold", 18)
    p.drawString(40, height - 50, "ARTISTRY HUB")

    p.setFont("Helvetica", 10)
    p.drawString(40, height - 70, f"Invoice ID: {order.id}")
    p.drawString(40, height - 85, f"Date: {order.created_at.strftime('%d-%m-%Y')}")

    # ===== CUSTOMER =====
    p.drawString(40, height - 120, f"Customer: {order.user.username}")
    p.drawString(40, height - 135, f"Email: {order.user.email}")

    # ===== TABLE HEADER =====
    y = height - 180
    p.setFont("Helvetica-Bold", 11)
    p.drawString(40, y, "Product")
    p.drawString(280, y, "Qty")
    p.drawString(330, y, "Price")
    p.drawString(420, y, "Total")
    p.line(40, y - 5, 550, y - 5)

    # ===== ITEMS =====
    p.setFont("Helvetica", 10)
    y -= 25

    grand_total = Decimal("0.00")

    for item in order.items.all():
        line_total = item.price * item.quantity
        grand_total += line_total

        p.drawString(40, y, item.product.name)
        p.drawString(280, y, str(item.quantity))
        p.drawString(330, y, f"₹{item.price}")
        p.drawString(420, y, f"₹{line_total}")
        y -= 20

    # ===== TOTAL =====
    p.line(330, y - 10, 550, y - 10)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(330, y - 30, "Grand Total:")
    p.drawString(420, y - 30, f"₹{grand_total}")

    # ===== FOOTER =====
    p.setFont("Helvetica", 9)
    p.drawString(40, 40, "Thank you for shopping with Artistry Hub!")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def send_invoice_email(order, pdf_bytes):
    if not order.user.email:
        return

    email = EmailMessage(
        subject=f"Invoice for Order #{order.id}",
        body="Thank you for your purchase. Your invoice is attached.",
        from_email=settings.EMAIL_HOST_USER,
        to=[order.user.email],
    )

    email.attach(
        f"invoice_order_{order.id}.pdf",
        pdf_bytes,
        "application/pdf",
    )

    email.send()
