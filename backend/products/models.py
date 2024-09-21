from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)
    image = models.ImageField(upload_to='categories/', null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    stock = models.IntegerField(default=0, null=True)
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, null=True)
    image = models.ImageField(upload_to='products/', null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('S', 'Shipped'),
        ('F', 'Failed'),
        ('R', 'Refunded'),
        ('O', 'Out for Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    shipping_address = models.CharField(max_length=255, null=True)
    billing_address = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically calculate total price before saving the order
        self.total_price = sum(item.price * item.quantity for item in self.orderitem_set.all())
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price at the time of order

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def total_items(self):
        return sum(item.quantity for item in self.cartitem_set.all())

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
