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

	def create(self, request):
		data = request.data
		xlfile = data["teachers-attendance"]

		print("xfile: ",xlfile)
		wb = load_workbook(xlfile)
		ws = wb.active
		print(ws.title)

		teacherz = []
		for row in ws.iter_rows(min_row=2, max_col=9, max_row=12, values_only=True):
			teacherz.append(row)
			#print(api)
		#print(teacherz)
		
		teachers = []
		for i in range(len(teacherz)):
			teacher = {
				"date": f"{teacherz[i][0]}",
				"time_in": f"{teacherz[i][1]}",
				"time_out": f"{teacherz[i][2]}",
				"teacher": f"{teacherz[i][3]}",
				"status": f"{teacherz[i][4]}",
					}
			teachers.append(teacher)
		return teachers
