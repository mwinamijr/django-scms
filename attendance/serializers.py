from rest_framework import serializers
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter

from .models import AttendanceStatus, TeachersAttendance, StudentAttendance
from users.serializers import TeacherSerializer

class AttendanceStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = AttendanceStatus
		fields = "__all__"

class TeachersAttendanceSerializer(serializers.ModelSerializer):
	#teacher = serializers.SerializerMethodField(read_only=True)
	#status = serializers.SerializerMethodField(read_only=True)
	total_days_attended = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = TeachersAttendance
		fields = "__all__"

	def get_total_days_attended(self, obj):
		
		#print(obj)
		teacher = obj.teacher
		attendance = TeachersAttendance.objects.filter(teacher=teacher)
		#print(attendance)
		days = 0
		for i in attendance:
			if i.status.name == "Present":
				days += 1
		#days = TeachersAttendanceSerializer(obj.date, many=True).data
		return days
'''
	def get_teacher(self, obj):
		teacher = obj.teacher
		serializer = TeacherSerializer(teacher, many=False)
		return serializer.data

	def get_status(self, obj):
		status = obj.status
		serializer = AttendanceStatusSerializer(status, many=False)
		return serializer.data
		'''
