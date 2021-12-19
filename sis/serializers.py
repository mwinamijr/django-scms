from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import PhoneNumber, EmergencyContact, EmergencyContactNumber, GradeLevel, ClassYear, Student, \
    StudentHealthRecord, GradeScale, GradeScaleRule, SchoolYear, MessageToStudent


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = "__all__"


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = "__all__"


class EmergencyContactNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContactNumber
        fields = "__all__"


class GradeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeLevel
        fields = "__all__"


class ClassYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassYear
        fields = "__all__"


class StudentHealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentHealthRecord
        fields = "__all__"


class GradeScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeScale
        fields = "__all__"


class GradeScaleRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeScaleRule
        fields = "__all__"


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = "__all__"


class MessageToStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageToStudent
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    #grad_date = serializers.SerializerMethodField(read_only=True)
    #bday = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Student
        fields = "__all__"
    '''
    def get_grad_date(self, obj):
        grad_date = obj.grad_date
        return grad_date
    
    def get_bday(self, obj):
        bday = obj.bday
        return bday
    '''
class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
