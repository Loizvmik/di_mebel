from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_team, name='create_team'),
    path('get/', views.get_teams, name='get_teams'),
    path('get/<int:team_id>/', views.get_team_by_id, name='get_team_by_id'),
    path('update/<int:team_id>/', views.update_team, name='update_team'),
    path('delete/<int:team_id>/', views.delete_team, name='delete_team'),
    path('add-image/<int:team_id>/', views.add_image_to_team, name='add_image_to_team'),
]