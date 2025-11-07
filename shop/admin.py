from django.contrib import admin
from .models import Category, Product, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    search_fields = ('name', 'description')

admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
