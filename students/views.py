from rest_framework import generics

from .models import Student
from .serializers import StudentSerializer

class StudentListView(generics.ListCreateAPIView):
	queryset = Student.objects.all()
	serializer = StudentSerializer