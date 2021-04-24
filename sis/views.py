from rest_framework import viewsets

from .models import (
    PhoneNumber, EmergencyContact, EmergencyContactNumber, 
    GradeLevel, ClassYear, Student, StudentHealthRecord, 
    GradeScale, GradeScaleRule, SchoolYear, MessageToStudent)
from .serializers import (
	PhoneNumbertSerializer, EmergencyContactSerializer, EmergencyContactNumberSerializer, 
    GradeLevelSerializer, ClassYearSerializer, StudentSerializer, StudentHealthRecordSerializer, 
    GradeScaleSerializer, GradeScaleRuleSerializer, SchoolYearSerializer, MessageToStudentSerializer)

class PhoneNumberViewSet(viewsets.ModelViewSet):
	queryset = PhoneNumber.objects.all()
	serializer_class = PhoneNumberSerializer

class EmergencyContactViewSet(viewsets.ModelViewSet):
	queryset = EmergencyContact.objects.all()
	serializer_class = EmergencyContactSerializer


class EmergencyContactNumberViewSet(viewsets.ModelViewSet):
	queryset = EmergencyContactNumber.objects.all()
	serializer_class = EmergencyContactNumberSerializer


class GradeLevelViewSet(viewsets.ModelViewSet):
	queryset = GradeLevel.objects.all()
	serializer_class = GradeLevelSerializer


class ClassYearViewSet(viewsets.ModelViewSet):
	queryset = ClassYear.objects.all()
	serializer_class = ClassYearSerializer


class StudentViewSet(viewsets.ModelViewSet):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer

class StudentHealthRecordViewSet(viewsets.ModelViewSet):
	queryset = StudentHealthRecord.objects.all()
	serializer_class = StudentHealthRecordSerializer

class GradeScaleViewSet(viewsets.ModelViewSet):
	queryset = GradeScale.objects.all()
	serializer_class = GradeScaleSerializer

class GradeScaleRuleViewSet(viewsets.ModelViewSet):
	queryset = GradeScaleRule.objects.all()
	serializer_class = GradeScaleRuleSerializer

class SchoolYearViewSet(viewsets.ModelViewSet):
	queryset = SchoolYear.objects.all()
	serializer_class = SchoolYearSerializer

class MessageToStudentViewSet(viewsets.ModelViewSet):
	queryset = MessageToStudent.objects.all()
	serializer_class = MessageToStudentSerializer

