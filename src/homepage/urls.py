from django.urls import path, include
from . import views
from .views import homepage

urlpatterns = [
    path('', homepage, name='homepage'),
    path('team/', include('src.homepage.team.urls'))
]