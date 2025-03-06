from django.urls import path
from .views import create_furniture, upload_image, get_furniture, get_furniture_by_id, update_furniture, \
    delete_furniture

urlpatterns = [
    #path('furniture/', furniture_list, name='furniture_list'),
    path('create',create_furniture,name='create_furniture'),
    path('images', upload_image, name='upload_image'),
    path('get', get_furniture, name='get_furniture'),
    path('get/<int:furniture_id>/', get_furniture_by_id, name='get_furniture_by_id'),
    path('update/<int:furniture_id>/', update_furniture, name='update_furniture'),
    path('delete/<int:furniture_id>/', delete_furniture, name='delete_furniture')
]
