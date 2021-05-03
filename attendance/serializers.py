from rest_framework import serializers
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter

from .models import AttendanceStatus, TeachersAttendance, StudentAttendance

class AttendanceStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = AttendanceStatus
		fields = "__all__"

class TeachersAttendanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = TeachersAttendance
		fields = "__all__"

