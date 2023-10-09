from rest_framework import serializers

from .models import (
    Teacher,
    ClassYear,
    StudentsMedicalHistory,
    Student,
    GradeScale,
    GradeScaleRule,
    ClassRoom,
    GradeLevel,
    ClassLevel,
    Parent,
)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class ClassYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassYear
        fields = "__all__"


class ClassLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLevel
        fields = "__all__"


class GradeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeLevel
        fields = "__all__"


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = "__all__"


class StudentHealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsMedicalHistory
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
        model = ClassYear
        fields = "__all__"


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    grade_level = serializers.SerializerMethodField(read_only=True)
    class_of_year = serializers.SerializerMethodField(read_only=True)
    parent_guardian = serializers.SerializerMethodField(read_only=True)

    # bday = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Student
        fields = "__all__"

    def get_grade_level(self, obj):
        grade_level = obj.grade_level
        serializer = GradeLevelSerializer(grade_level, many=False)
        grade_level = serializer.data["name"]
        return grade_level

    def get_class_of_year(self, obj):
        class_of_year = obj.class_of_year
        serializer = ClassYearSerializer(class_of_year, many=False)
        class_of_year = serializer.data["full_name"]
        return class_of_year

    def get_parent_guardian(self, obj):
        parent_guardian = obj.parent_guardian
        serializer = ParentSerializer(parent_guardian, many=False)
        parent_guardian = serializer.data["email"]
        return parent_guardian

    def create(self, request):
        data = request.data
        student = Student()
        student.first_name = data["first_name"]
        student.middle_name = data["middle_name"]
        student.last_name = data["last_name"]
        student.admission_number = data["addmission_number"]
        student.parent_contact = data["parent_contact"]
        student.region = data["region"]
        student.city = data["city"]
        student.street = data["street"]
        student.grade_level = GradeLevel.objects.get(name=data["grade_level"])
        student.gender = data["gender"]
        student.date_of_birth = data["date_of_birth"]
        print(data["date_of_birth"])
        # student.class_of_year = ClassYear.objects.get(year=data['class_of_year'])
        student.save()
        return student

    def bulk_create(self, student):
        data = student
        print(data)
        student = Student()
        student.first_name = data["first_name"].lower()
        student.middle_name = data["middle_name"].lower()
        student.last_name = data["last_name"].lower()
        student.admission_number = data["addmission_number"]
        student.parent_contact = data["parent_contact"]
        student.grade_level = GradeLevel.objects.get(name=data["grade_level"])
        student.gender = data["gender"]
        student.date_of_birth = "2000-01-01"
        # student.class_of_year = ClassYear.objects.get(year=data['class_of_year'])
        student.save()
        return student
