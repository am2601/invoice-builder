from django.contrib import admin
from .models import Product, Invoice, UserProfile


admin.site.register(UserProfile)
admin.site.register(Invoice)
admin.site.register(Product)
