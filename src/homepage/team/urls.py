from django.urls import path
from . import view

urlpatterns = [
    path('', view.get_team, name='get_team'),
    path('put/<int:team_id>/', view.update_team_image, name='update_team_image'),
    path('create/', view.create_team, name='create_team'),
    path('get/<int:team_id>/', view.get_team_by_id, name='get_team_by_id'),
    path('update/<int:team_id>/', view.update_team, name='update_team'),
    path('delete/<int:team_id>/', view.delete_team, name='delete_team'),
]