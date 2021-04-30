from rest_framework import viewsets

from .models import Accountant, Teacher
from .serializers import (
	AccountantSerializer, TeacherSerializer)

class AccountantViewSet(viewsets.ModelViewSet):
	queryset = Accountant.objects.all()
	serializer_class = AccountantSerializer

class TeacherViewSet(viewsets.ModelViewSet):
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer

