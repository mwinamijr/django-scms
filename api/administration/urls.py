from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
	ArticleViewSet, CarouselImageViewSet)

from attendance.views import (
	AttendanceStatusViewSet, TeachersAttendanceViewSet, 
	TeachersAttendanceListView, TeachersAttendanceDetailView,TeachersAttendanceBulkCreateView)

from schedule.views import (
	PeriodViewSet, SubjectViewSet, DailyTimeTableViewSet, WeeklyTimeTableViewSet)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'carousel', CarouselImageViewSet)
router.register(r'status', AttendanceStatusViewSet)
router.register(r'teachers-attendance', TeachersAttendanceViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'daily-timetable', DailyTimeTableViewSet)
router.register(r'weekly-timetable', WeeklyTimeTableViewSet)

urlpatterns = [
	path('', include(router.urls))
]