from django.contrib import admin
from .models import User, Category, Book, CartItem

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(CartItem)
