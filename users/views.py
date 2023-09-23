from rest_framework import generics, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from django.http import Http404


from attendance.models import TeachersAttendance
from attendance.serializers import (TeachersAttendanceSerializer)

from .models import CustomUser as User

from .models import Accountant
from .serializers import ( UserSerializer, UserSerializerWithToken, AccountantSerializer)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        print(data)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListView(views.APIView):
    """
    List all users, or create a new user.
    """
    #permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        print(serializer.is_valid())
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(views.APIView):

    #permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AccountantListView(views.APIView):
    """
    List all accountants
    """
    #permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        accontants = Accountant.objects.all()
        serializer = AccountantSerializer(accontants, many=True)
        return Response(serializer.data)

class AccountantDetailView(views.APIView):

    #permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Accountant.objects.get(pk=pk)
        except Accountant.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        accountant = self.get_object(pk)
        serializer = AccountantSerializer(accountant)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        accountant = self.get_object(pk)
        serializer = AccountantSerializer(accountant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        accountant = self.get_object(pk)
        accountant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)	