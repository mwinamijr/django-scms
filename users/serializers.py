from rest_framework import serializers

from .models import Accountant, Teacher, CustomUser

class AccountantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accountant
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"