from django.contrib import admin
from .models import Furniture, Image, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    inlines = [ProductImageInline]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
