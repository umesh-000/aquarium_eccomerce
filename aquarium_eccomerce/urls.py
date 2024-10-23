from django.conf.urls.static import static
from django.conf.urls import handler404
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', include('accounts.urls')),
    
    path('mysite/', include('mysite.urls')),
    
    path('admin/', include('myadmin.urls')),
]

handler404 = 'mysite.views.custom_404'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)