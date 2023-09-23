from rest_framework import generics, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password
from django.http import Http404

from .models import Teacher
from .serializers import (TeacherSerializer)

class TeacherListView(views.APIView):
    """
    List all teachers
    """
    #permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

class TeacherDetailView(views.APIView):

    #permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        teacher = self.get_object(pk)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)	
