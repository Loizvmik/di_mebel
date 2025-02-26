from django.urls import path
from .views import create_furniture,upload_image,image_list_slider

urlpatterns = [
    #path('furniture/', furniture_list, name='furniture_list'),
    path('create',create_furniture,name='create_furniture'),
    path('images', upload_image, name='upload_image'),
    path('images/slider', image_list_slider, name='image_list_slider')
]
