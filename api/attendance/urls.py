from django.urls import path, include
from rest_framework.routers import DefaultRouter
from attendance.views import (
	AttendanceStatusViewSet, TeachersAttendanceViewSet, 
	TeachersAttendanceListView, TeachersAttendanceDetailView,
	TeachersAttendanceBulkUploadView, teacherAttendanceView, dailyAttendanceView)

'''
router = DefaultRouter()
router.register(r'status', AttendanceStatusViewSet)
router.register(r'teachers-attendance', TeachersAttendanceViewSet)

urlpatterns = [
	path('', include(router.urls))
]
'''

urlpatterns = [
	path('teachers-attendance/', TeachersAttendanceListView.as_view(), name="teachers-attendance-list"),
    path('teachers-attendance/<int:pk>/', TeachersAttendanceDetailView.as_view(), name="teachers-attendance-detail"),
    path('teacher-attendance/<int:pk>/', teacherAttendanceView, name="teacher-attendance-list"),
    path('teacher-attendances/', dailyAttendanceView, name="teacher-attendance-by-date"),
	path("teachers-attendance/upload/<filename>/", TeachersAttendanceBulkUploadView.as_view(), name="teachers-attendance-bulk"),
]