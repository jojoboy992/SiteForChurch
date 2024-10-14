
from django.contrib import admin
from django.urls import path, include , re_path
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.views.static import serve
from homepage.views import *

handler404 = 'homepage.views.custom_404'

urlpatterns = [
    path('x1_x1_x1_admin_woggwc_x1_x1_x1_jojoboy_x1_x1_x1/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')),
    # path('jet/', include('jet.urls', 'jet')), 
    path('', include('homepage.urls')),
]

# Serve media files
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# Serve static files in development only
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


