from django.urls import path, include
from rest_framework.routers import DefaultRouter
from attendance.views import (
	AttendanceStatusViewSet, TeachersAttendanceViewSet)

router = DefaultRouter()
router.register(r'status', AttendanceStatusViewSet)
router.register(r'teachers-attendance', TeachersAttendanceViewSet)

urlpatterns = [
	path('', include(router.urls))
]