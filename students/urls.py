from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import StudentListView, StudentDetailView


urlpatterns = [
	path('', StudentListView.as_view(), name="students-list"),
	path('<int:pk>/', StudentDetailView.as_view(), name="student-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)