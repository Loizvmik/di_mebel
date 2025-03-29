from django.contrib import admin
from src.homepage.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_image_display')
    search_fields = ('name', 'description')
    list_filter = ('name',)

    def get_image_display(self, obj):
        """Отображает информацию об изображении в списке команд"""
        if obj.image:
            return f"Image ID: {obj.image.id}"
        return "Нет изображения"

    get_image_display.short_description = 'Изображение'