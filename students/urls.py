from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import StudentListView


urlpatterns = [
	path('', StudentListView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)