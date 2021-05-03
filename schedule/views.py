from rest_framework import generics, views, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import (
    Subject, Period, DailyTimeTable, WeeklyTimeTable)

from .serializers import (
	SubjectSerializer, PeriodSerializer, DailyTimeTableSerializer, WeeklyTimeTableSerializer
	)

class SubjectViewSet(viewsets.ModelViewSet):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer

class PeriodViewSet(viewsets.ModelViewSet):
	queryset = Period.objects.all()
	serializer_class = PeriodSerializer

class DailyTimeTableViewSet(viewsets.ModelViewSet):
	queryset = DailyTimeTable.objects.all()
	serializer_class = DailyTimeTableSerializer

class WeeklyTimeTableViewSet(viewsets.ModelViewSet):
	queryset = WeeklyTimeTable.objects.all()
	serializer_class = WeeklyTimeTableSerializer
