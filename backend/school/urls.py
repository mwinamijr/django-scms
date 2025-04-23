from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
import debug_toolbar
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html"),name="home"),
    path("api/academic/", include("api.academic.urls")),
    path("api/administration/", include("api.administration.urls")),
    path("api/attendance/", include("api.attendance.urls")),
    path("api/assignments/", include("api.assignments.urls")),
    path("api/blog/", include("api.blog.urls")),
    path("api/finance/", include("api.finance.urls")),
    # path('api/journals/', include('api.journals.urls')),
    # path("api/notes/", include("api.notes.urls")),
    path("api/users/", include("api.users.urls")),
    path("api/timetable/", include("api.schedule.urls")),
    path("api/sis/", include("api.sis.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
    path('', csrf_exempt(TemplateView.as_view(template_name='index.html'))),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
