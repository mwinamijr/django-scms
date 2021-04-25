from django.db import models
import httpagentparser


from users.models import CustomUser, Teacher
from sis.models import GradeLevel

from datetime import datetime

class Article(models.Model):
	title = models.CharField(max_length=150, blank=True, null=True)
	content = models.TextField(blank=True, null=True)
	picture = models.ImageField(upload_to="articles", blank=True, null=True)

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
    ua = models.CharField(max_length=2000, help_text="User agent. We can use this to determine operating system and browser in use.")
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

class ClassEnrollment(models.Model):
    class_section = models.ForeignKey('ClassSection', on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey('sis.Student', on_delete=models.CASCADE, blank=True, null=True)
    attendance_note = models.CharField(max_length=255, blank=True, help_text="This note will appear when taking attendance.")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (("class_section", "student"),)


class ClassTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    class_section = models.ForeignKey('ClassSection', on_delete=models.CASCADE, blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher', 'class_section')


class ClassSection(models.Model):
    gradeLevel = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, blank=True, null=True)
    section = models.CharField(max_length=1, choices=(('A', 'A'), ('B', 'B'),('C', 'C')))
    teacher = models.ForeignKey(Teacher, through=ClassTeacher,on_delete=models.CASCADE, blank=True, null=True)
    students = models.ManyToManyField('sis.Student', blank=True, null=True)