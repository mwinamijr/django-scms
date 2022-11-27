from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import PhoneNumber, EmergencyContact, EmergencyContactNumber, GradeLevel, ClassLevel, ClassYear, Student, \
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

class ClassLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLevel
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
    grade_level = serializers.SerializerMethodField(read_only=True)
    class_level = serializers.SerializerMethodField(read_only=True)
    class_of_year = serializers.SerializerMethodField(read_only=True)
    #emergency_contacts = serializers.SerializerMethodField(read_only=True)
    #bday = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Student
        fields = "__all__"

    def get_grade_level(self, obj):
        grade_level = obj.grade_level
        serializer = GradeLevelSerializer(grade_level, many=False)
        grade_level = serializer.data['name']
        return grade_level

    def get_class_level(self, obj):
        class_level = obj.class_level
        serializer = ClassLevelSerializer(class_level, many=False)
        class_level = serializer.data['name']
        return class_level

    def get_class_of_year(self, obj):
        class_of_year = obj.class_of_year
        serializer = ClassYearSerializer(class_of_year, many=False)
        class_of_year = serializer.data['full_name']
        return class_of_year

    def create(self, request):
        data= request.data
        student = Student()
        student.first_name = data['first_name']
        student.middle_name = data['middle_name']
        student.last_name = data['last_name']
        student.addmission_number = data['addmission_number']
        student.region = data['region']
        student.city = data['city']
        student.street = data['street']
        student.prems_number = data['prems_number']
        student.std_vii_number = data['std_vii_number']
        student.grade_level = GradeLevel.objects.get(name=data['grade_level'])
        student.class_level = ClassLevel.objects.get(name=data['class_level'])
        student.birthday = data['birthday']
        print(data['birthday'])
        student.class_of_year = ClassYear.objects.get(year=data['class_of_year'])
        student.save()
        return student

    def bulk_create(self, request):
        data = request.data
        student = Student()
        student.addmission_number = data['addmission_number']
        student.first_name = data['first_name']
        student.middle_name = data['middle_name']
        student.last_name = data['last_name']
        student.grade_level = GradeLevel.objects.get(name=data['grade_level'])
        student.class_level = ClassLevel.objects.get(name=data['class_level'])
        student.birthday = data['birthday']
        print(data['birthday'][:10])
        #student.grad_date = data['grad_date']
        student.region = data['region']
        student.city= data['city']
        student.street = data['street']
        student.prems_number = data['prems_number']
        student.sex = data['sex']
        student.std_vii_number = data['std_vii_number']

        #student.save()
        return student


    
class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
