from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', TemplateView.as_view(template_name='index.html')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/administrations/', include('api.administration.urls')),
    path('api/users/', include('api.users.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
