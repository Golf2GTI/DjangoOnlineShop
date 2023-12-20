from django.contrib import admin
from .models import Product, CustomUser, ProductImage

admin.site.register(Product)
admin.site.register(CustomUser)
admin.site.register(ProductImage)
# Register your models here.
