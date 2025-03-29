from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_vacancy_view, name='create_vacancy'),
    path('delete/<int:vacancy_id>/', views.delete_vacancy_view, name='delete_vacancy'),
    path('vacancy_person/create/', views.create_vacancy_person_view, name='create_vacancy_person'),
    path('vacancy_person/delete/<str:phone>/', views.delete_vacancy_person_by_phone_view, name='delete_vacancy_person_by_phone'),
]