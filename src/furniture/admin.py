from django.contrib import admin
from .models import Furniture, Image, Color, FurnitureColor


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1



class FurnitureColorInline(admin.TabularInline):
    model = FurnitureColor
    extra = 1
    verbose_name = "Цвет"
    verbose_name_plural = "Цвета"


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    inlines = [ImageInline, FurnitureColorInline]
    filter_horizontal = ('colors',)  # для удобного выбора цветов



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')



@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'get_furniture_count')
    search_fields = ('name',)

    def get_furniture_count(self, obj):
        """Отображает количество мебели, связанной с этим цветом"""
        return obj.furnitures.count()

    get_furniture_count.short_description = 'Количество мебели'

