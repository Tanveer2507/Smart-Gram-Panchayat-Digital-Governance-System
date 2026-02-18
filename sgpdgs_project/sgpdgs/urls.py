from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import admin customization
from .admin import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('complaints/', include('complaints.urls')),
    path('certificates/', include('certificates.urls')),
    path('budget/', include('budget.urls')),
    path('notices/', include('notices.urls')),
    path('notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
