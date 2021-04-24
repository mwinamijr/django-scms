from rest_framework import serializers

from .models import Accountant, Teacher

class AccountantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accountant
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"