from rest_framework import viewsets

from .models import AttendanceStatus, TeachersAttendance
from .serializers import (
	AttendanceStatusSerializer, TeachersAttendanceSerializer)

class AttendanceStatusViewSet(viewsets.ModelViewSet):
	queryset = AttendanceStatus.objects.all()
	serializer_class = AttendanceStatusSerializer

class TeachersAttendanceViewSet(viewsets.ModelViewSet):
	queryset = TeachersAttendance.objects.all()
	serializer_class = TeachersAttendanceSerializer

