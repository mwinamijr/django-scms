from rest_framework import generics, views, viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter

from .models import AttendanceStatus, TeachersAttendance
from .serializers import (
	AttendanceStatusSerializer, TeachersAttendanceSerializer)

class AttendanceStatusViewSet(viewsets.ModelViewSet):
	queryset = AttendanceStatus.objects.all()
	serializer_class = AttendanceStatusSerializer

class TeachersAttendanceViewSet(viewsets.ModelViewSet):
	queryset = TeachersAttendance.objects.all()
	serializer_class = TeachersAttendanceSerializer

class TeachersAttendanceBulkUploadView(views.APIView):
	"""
	This uploads bulk daily teacher's attendance from an excel file
	"""

	parser_class = [FileUploadParser]
	def post(self, request, filename, format="xlsx"):
		file_obj = request.data
		xlfile = file_obj["filename"]

		#print(xlfile)
		wb = load_workbook(xlfile)
		ws = wb.active
		#print(ws.title)

		studentz = []
		for row in ws.iter_rows(min_row=2, max_col=9, max_row=12, values_only=True):
			studentz.append(row)
			#print(api)
			
		students = []
		for i in range(len(studentz)):
			student = {
				"date": f"{studentz[i][0]}",
				"time_in": f"{studentz[i][1]}",
				"time_out": f"{studentz[i][2]}",
				"teacher": f"{studentz[i][3]}",
				"status": f"{studentz[i][4]}",
					}
			students.append(student)
		
		for student in students:
			if student in Student.objects.all():
				print("student exists!")
				continue
			else: 
				serializer = StudentSerializer(data=student)
				if serializer.is_valid():
					serializer.save()
					#return Response(serializer.data, status=status.HTTP_201_CREATED)
				#return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


		#print(students)


		student = Student()


		return Response(status=204)


