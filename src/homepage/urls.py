from django.urls import path, include

urlpatterns = [
    path('team/', include('src.homepage.team.urls')),
    # Другие URL-пути для homepage
]