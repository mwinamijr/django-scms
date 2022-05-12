from django.db import models
import httpagentparser
from django.conf import settings

from users.models import CustomUser, Teacher
from sis.models import GradeLevel, ClassLevel

from datetime import datetime


class Article(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to="articles", blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CarouselImage(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to="carousel")

    def __str__(self):
        return self.title


class AccessLog(models.Model):
    login = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    ua = models.CharField(max_length=2000,
                          help_text="User agent. We can use this to determine operating system and browser in use.")
    date = models.DateTimeField(default=datetime.now)
    ip = models.GenericIPAddressField()
    usage = models.CharField(max_length=255)

    def __str__(self):
        return str(self.login) + " " + str(self.usage) + " " + str(self.date)

    def os(self):
        try:
            return httpagentparser.simple_detect(self.ua)[0]
        except:
            return "Unknown"

    def browser(self):
        try:
            return httpagentparser.simple_detect(self.ua)[1]
        except:
            return "Unknown"


class ClassTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    class_section = models.ForeignKey('ClassSection', on_delete=models.CASCADE, blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher', 'class_section')

    def __str__(self):
        return f"{self.teacher}-{self.class_section}"


class ClassSection(models.Model):
    classLevel = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, blank=True, null=True)
    section = models.CharField(max_length=1, choices=(('A', 'A'), ('B', 'B'), ('C', 'C')))
    students = models.ManyToManyField('sis.Student', blank=True)
    year = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.classLevel} {self.section}"


class ClassJournal(models.Model):
    date = models.DateField(blank=True, null=True, validators=settings.DATE_VALIDATORS)
    class_section = models.ForeignKey(ClassSection, on_delete=models.SET_NULL, blank=True, null=True)
    periods = models.ForeignKey('schedule.DailyTimeTable', on_delete=models.SET_NULL, blank=True, null=True)
    absent_students = models.ManyToManyField('sis.Student', blank=True)

    class Meta:
        ordering = ('-date',)
        unique_together = ('date',)

    def __str__(self):
        return f"{self.date}-{self.class_section} "
