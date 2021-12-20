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

from schedule.models import Period, WeeklyTimeTable, DailyTimeTable

from .models import Accountant, Teacher
from .serializers import ( UserSerializer, UserSerializerWithToken,
	AccountantSerializer, AccountantSerializerWithToken, TeacherSerializer)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


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




@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    user = User.objects.get(id=pk)

    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')