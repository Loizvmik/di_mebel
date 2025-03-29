from django.contrib import admin
from .models import Furniture, Color, Image

@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    filter_horizontal = ('colors',)  # для удобного выбора цветов

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
