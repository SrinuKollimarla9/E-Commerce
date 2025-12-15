from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('orders/', views.order_history, name='order_history'),
    path("orders/<int:order_id>/", views.order_confirmation, name="order_detail"),
    path('place-order/', views.place_order, name='place_order'),
    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='shop/login.html'),name='login'),


    # AUTH URLS (MUST BE PRESENT)
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
