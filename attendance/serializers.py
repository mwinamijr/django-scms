from rest_framework import serializers
from .models import AttendanceStatus, TeachersAttendance, StudentAttendance

class AttendanceStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = AttendanceStatus
		fields = "__all__"

class TeachersAttendanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = TeachersAttendance
		fields = "__all__"

