from rest_framework import serializers

from .models import PhoneNumber, EmergencyContact, EmergencyContactNumber, GradeLevel, ClassYear, Student, StudentHealthRecord, GradeScale, GradeScaleRule, SchoolYear, MessageToStudent

class PhoneNumbertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = "__all__"

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = "__all__"

class EmergencyContacNumbertSerializer(serializers.ModelSerializer):
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


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
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

