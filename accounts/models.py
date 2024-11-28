from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone


class User(AbstractUser):
    gender = models.CharField(max_length=100, default="Male")
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    is_seller = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True, default='')
    # first_name = models.CharField(_("first name"), max_length=150)
    # last_name = models.CharField(_("last name"), max_length=150)


class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'street_address', 'city', 'state', 'pincode', 'country')

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.pincode}, {self.country}"


class Product(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quality = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.name

    def reduce_stock(self, quantity):
        if self.stock_quality>=quantity:
            self.stock_quality-=quantity
            self.save()
        else:
            raise ValueError("Insufficient Stock Available")


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=30, choices=[('pending', 'Pending'), ('shipped', 'shipped'), ('delivered', 'delivered'), ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True,  blank=True)

    def __str__(self):
        return f"order{self.id} for {self.product.name} by {self.user.username}"

    def decrease_product_stock(self):
        self.product.reduce_stock(self.quantity)













