from django.urls import path
from .views import create_furniture,upload_image

urlpatterns = [
    #path('furniture/', furniture_list, name='furniture_list'),
    path('create',create_furniture,name='create_furniture'),
    path('images', upload_image, name='upload_image'),
]
