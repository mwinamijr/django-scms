from django.contrib import admin

from .models import (
    ClassYear, EmergencyContact, 
    EmergencyContactNumber, GradeLevel, ClassLevel,
    GradeScale, GradeScaleRule, SchoolYear,
    Student, StudentHealthRecord, MessageToStudent
    )

admin.site.register(ClassYear)
admin.site.register(EmergencyContact)
admin.site.register(EmergencyContactNumber)
admin.site.register(GradeLevel)
admin.site.register(ClassLevel)
admin.site.register(GradeScale)
admin.site.register(GradeScaleRule)
admin.site.register(SchoolYear)
admin.site.register(Student)
admin.site.register(StudentHealthRecord)
admin.site.register(MessageToStudent)
