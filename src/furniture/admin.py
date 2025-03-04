from django.contrib import admin
from .models import Furniture, Image


class ImageInline(admin.TabularInline):  # или admin.StackedInline, если предпочитаете другой вид отображения
    model = Image
    extra = 1

@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    inlines = [ImageInline]
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')

