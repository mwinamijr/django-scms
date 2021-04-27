from rest_framework import viewsets, views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status

from .models import (
    PhoneNumber, EmergencyContact, EmergencyContactNumber, 
    GradeLevel, ClassYear, Student, StudentHealthRecord, 
    GradeScale, GradeScaleRule, SchoolYear, MessageToStudent)

from .serializers import (
	PhoneNumberSerializer, EmergencyContactSerializer, EmergencyContactNumberSerializer, 
    GradeLevelSerializer, ClassYearSerializer, StudentSerializer, StudentHealthRecordSerializer, 
    GradeScaleSerializer, GradeScaleRuleSerializer, SchoolYearSerializer, MessageToStudentSerializer)
'''
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
'''



class StudentListView(views.APIView):
	"""
    List all students, or create a new student.
    """
	def get(self, request, format=None):
		students = Student.objects.all()
		serializer = StudentSerializer(students, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = StudentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailView(views.APIView):
	def get_object(self, pk):
		try:
			return Student.objects.get(pk=pk)
		except Student.DoesNotExist:
			raise Http404
	def get(self, request, pk, format=None):
		student = self.get_object(pk)
		serializer = StudentSerializer(student)
		return Response(serializer.data)
		
	def put(self, request, pk, format=None):
		student = self.get_object(pk)
		serializer = StudentSerializer(student, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		student = self.get_object(pk)
		student.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class StudentBulkUploadView(views.APIView):
	parser_class = [FileUploadParser]
	def post(self, request, filename, format=None):
		file_obj = request.data['file']

		return Response(status=204)


'''
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
'''
