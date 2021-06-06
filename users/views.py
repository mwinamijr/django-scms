from django.db import models
from rest_framework import generics, views, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
import json

from attendance.models import TeachersAttendance
from attendance.serializers import (TeachersAttendanceSerializer)

from schedule.models import Period, WeeklyTimeTable, DailyTimeTable

from .models import Accountant, Teacher
from .serializers import (
	AccountantSerializer, TeacherSerializer)

class AccountantViewSet(viewsets.ModelViewSet):
	queryset = Accountant.objects.all()
	serializer_class = AccountantSerializer

class TeacherViewSet(viewsets.ModelViewSet):
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer


@api_view(['GET'])
def teacherProfileView(request, pk):
	try:
		teacher = Teacher.objects.get(pk=pk)
	except TeachersAttendance.DoesNotExist:
		raise Http404
	####
	start_date='2021-04-01'
	end_date='2021-04-30'

	weeklyPeriods = DailyTimeTable.objects.all()
	#print(weeklyPeriods)
	teacherPeriods = []
	#periods1 = weeklyPeriods.filter(period)
	periods = weeklyPeriods.filter(period1=3)
	p1= periods[0]
	print(type(p1))
	print(p1)
	
	for dailyPeriods in weeklyPeriods:
		print(dailyPeriods.period1)
		for period in dailyPeriods.objects.all():
			print(period)
	
	
	#print(mondayPeriods)

	attendances = TeachersAttendance.objects.filter(teacher=teacher)
	attended_days = TeachersAttendance.objects.filter(teacher=teacher, date__gte=start_date, date__lte=end_date, status=1).count()
	absent_days = len(TeachersAttendance.objects.filter(teacher=teacher, date__gte=start_date, date__lte=end_date, status=2))
	sick_days = len(TeachersAttendance.objects.filter(teacher=teacher, date__gte=start_date, date__lte=end_date, status=3))

	serializer = TeachersAttendanceSerializer(attendances, many=True)
	try:
		teacher = serializer.data[0]['teacher']
	except:
		teacher = "No teacher"
	return Response({
		'teacher': teacher,
		'attended_days': attended_days,
		'absent_days': absent_days + sick_days
		})

	####