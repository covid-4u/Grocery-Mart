from django.contrib import admin
from .models import Category,Product,Cart,CartItem,Order
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)