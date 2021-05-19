from rest_framework import generics, views, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter
import json

from users.models import Teacher
from .models import ClassJournal
from .serializers import (ClassJournalSerializer)

class ClassJournalListView(views.APIView):
	"""
    List all ClassJournals, or create a new ClassJournal.
    """
	def get(self, request, format=None):
		attendances = ClassJournal.objects.all()
		serializer = ClassJournalSerializer(attendances, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = ClassJournalSerializer(data=request.data)
		print(request.data)
		print(serializer.is_valid())
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassJournalDetailView(views.APIView):
	def get_object(self, pk):
		try:
			return ClassJournal.objects.get(pk=pk)
		except TeachersAttendance.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		attendance = self.get_object(pk)
		serializer = ClassJournalSerializer(attendance)
		return Response(serializer.data)
		
	def put(self, request, pk, format=None):
		attendance = self.get_object(pk)
		serializer = ClassJournalSerializer(attendance, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		attendance = self.get_object(pk)
		attendance.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

