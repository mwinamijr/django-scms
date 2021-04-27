from django.urls import path, include
from sis.views import (
    #PhoneNumberViewSet, EmergencyContactViewSet, EmergencyContactNumberViewSet, 
    #GradeLevelViewSet, ClassYearViewSet, StudentHealthRecordViewSet, GradeScaleViewSet, 
    #GradeScaleRuleViewSet, SchoolYearViewSet, MessageToStudentViewSet, 
    StudentListView, StudentDetailView, StudentBulkUploadView
)


urlpatterns = [
    path('students/', StudentListView.as_view(), name="students-list"),
    path('students/<int:pk>/', StudentDetailView.as_view(), name="student-detail"),
    path('upload/<filename>/', StudentBulkUploadView.as_view()),
    ]

'''
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
'''
