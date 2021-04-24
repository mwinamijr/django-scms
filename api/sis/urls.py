from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sis.views import (
    PhoneNumberViewSet, EmergencyContactViewSet, EmergencyContactNumberViewSet, 
    GradeLevelViewSet, ClassYearViewSet, StudentViewSet, StudentHealthRecordViewSet, GradeScaleViewSet, 
    GradeScaleRuleViewSet, SchoolYearViewSet, MessageToStudentViewSet
)

router = DefaultRouter()
router.register(r'phonenumber', PhoneNumberViewSet)
router.register(r'emergencyContact', EmergencyContactViewSet)
router.register(r'emergencyContactNumber', EmergencyContactNumberViewSet)
router.register(r'gradeLevels', GradeLevelViewSet)
router.register(r'classYear', ClassYearViewSet)
router.register(r'students', StudentViewSet)
router.register(r'studentsHealthRecord', StudentHealthRecordViewSet)
router.register(r'gradeScale', GradeLevelViewSet)
router.register(r'gradeScaleRule', GradeScaleRuleViewSet)
router.register(r'schoolYear', SchoolYearViewSet)
router.register(r'messageToStudents', MessageToStudentViewSet)

urlpatterns = [
	path('', include(router.urls))
]