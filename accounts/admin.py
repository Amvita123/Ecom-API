from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Order, Address


class User_Admin(UserAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_seller', 'gender', 'phone_no']


admin.site.register(User, User_Admin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'description', 'stock_quality']


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'status', 'created_at', 'address']


admin.site.register(Order, OrderAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street_address', 'city', 'state', 'pincode', 'country']


admin.site.register(Address, AddressAdmin)
