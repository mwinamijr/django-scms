from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    ArticleViewSet, CarouselImageViewSet)

from attendance.views import (
    AttendanceStatusViewSet, TeachersAttendanceViewSet,
    TeachersAttendanceListView, TeachersAttendanceDetailView, TeachersAttendanceBulkCreateView)
from notes.views import TopicViewSet, SubTopicViewSet, AssignmentViewSet
from schedule.views import (
    PeriodViewSet, SubjectViewSet, DailyTimeTableViewSet, WeeklyTimeTableViewSet)

from users.views import AccountantViewSet, TeacherViewSet

router = DefaultRouter()
router.register(r'users/accountants', AccountantViewSet)
router.register(r'users/teachers', TeacherViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'carousel', CarouselImageViewSet)
router.register(r'status', AttendanceStatusViewSet)
router.register(r'teachers-attendance', TeachersAttendanceViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'daily-timetable', DailyTimeTableViewSet)
router.register(r'weekly-timetable', WeeklyTimeTableViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubTopicViewSet)
router.register(r'assignments', AssignmentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
