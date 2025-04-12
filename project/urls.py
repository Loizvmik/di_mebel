from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('furniture/', include('src.furniture.urls')),
    path('', include('src.homepage.urls')),
    path('vacancy/', include('src.vacancy.urls')),
    path('homepage/', include('src.homepage.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)