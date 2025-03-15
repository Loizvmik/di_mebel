from django.urls import path
from .views import create_furniture, upload_image, get_furniture, get_furniture_by_id, update_furniture_data, \
    delete_furniture, add_furniture_images, update_furniture_images, get_colors, create_color, delete_color

urlpatterns = [
    #path('furniture/', furniture_list, name='furniture_list'),
    path('create',create_furniture,name='create_furniture'),
    path('images', upload_image, name='upload_image'),
    path('get', get_furniture, name='get_furniture'),
    path('get/<int:furniture_id>/', get_furniture_by_id, name='get_furniture_by_id'),
    path('update/data/<int:furniture_id>/', update_furniture_data, name='update_furniture_data'),
    path('update/images/add/<int:furniture_id>/',add_furniture_images, name='add_furniture_images'),
    path('update/images/replace/<int:furniture_id>/', update_furniture_images, name='update_furniture_images'),
    path('delete/<int:furniture_id>/', delete_furniture, name='delete_furniture'),
    path('get/colors/', get_colors, name='get_colors'),
    path('create/colors/',create_color, name='create_color'),
    path('delete/colors/<int:color_id>/', delete_color, name='delete_color')
]
