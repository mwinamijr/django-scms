from django.contrib import admin

from .models import (
    ClassYear, ClassLevel,
    GradeScale, GradeScaleRule, SchoolYear,
    Student, StudentHealthRecord
    )

admin.site.register(ClassYear)
admin.site.register(ClassLevel)
admin.site.register(SchoolYear)
admin.site.register(Student)
admin.site.register(StudentHealthRecord)
