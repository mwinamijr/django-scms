from django.db import models
import httpagentparser

from users.models import Teacher
from sis.models import GradeLevel, ClassLevel
from administration.models import ClassSection

TIMETABLE_CHOICES = [
    ("1", "07:20:00 - 08:00:00"),
    ("2", "08:00:00 - 08:40:00"),
    ("3", "08:40:00 - 09:20:00"),
    ("4", "09:20:00 - 10:00:00"),
    ("5", "10:20:00 - 11:00:00"),
    ("6", "11:00:00 - 11:40:00"),
    ("7", "11:40:00 - 12:20:00"),
    ("8", "12:20:00 - 13:00:00"),
]

class Subject(models.Model):
    code = models.IntegerField(primary_key=True,blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=5, blank=True, null=True)
    
    def __str__(self):
        return self.short_name

class Period(models.Model):
    subject = models.OneToOneField(Subject, related_name='period', on_delete=models.CASCADE)
    _class = models.ForeignKey(ClassLevel, blank=True, default=1, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    period_time = models.CharField(max_length=100, choices=TIMETABLE_CHOICES, blank=True, null=True)
    taught = models.BooleanField(default=False)

    class Meta:
        ordering = ('id', 'period_time',)

    def __str__(self):
        return f"{self.subject} - {self.teacher}-{self._class}"


class DailyTimeTable(models.Model):
    period1 = models.ForeignKey(Period, related_name='period1', on_delete=models.CASCADE, blank=True, null=True)
    period2 = models.ForeignKey(Period, related_name='period2', on_delete=models.CASCADE, blank=True, null=True)
    period3 = models.ForeignKey(Period, related_name='period3', on_delete=models.CASCADE, blank=True, null=True)
    period4 = models.ForeignKey(Period, related_name='period4', on_delete=models.CASCADE, blank=True, null=True)
    period5 = models.ForeignKey(Period, related_name='period5', on_delete=models.CASCADE, blank=True, null=True)
    period6 = models.ForeignKey(Period, related_name='period6', on_delete=models.CASCADE, blank=True, null=True)
    period7 = models.ForeignKey(Period, related_name='period7', on_delete=models.CASCADE, blank=True, null=True)
    period8 = models.ForeignKey(Period, related_name='period8', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.period1} / {self.period8}"


class WeeklyTimeTable(models.Model):
    monday = models.OneToOneField(DailyTimeTable,related_name='monday', on_delete=models.CASCADE, blank=True, null=True)
    tuesday = models.OneToOneField(DailyTimeTable,related_name='tuesday', on_delete=models.CASCADE, blank=True, null=True)
    wednesday = models.OneToOneField(DailyTimeTable,related_name='wednesday', on_delete=models.CASCADE, blank=True, null=True)
    thursday = models.OneToOneField(DailyTimeTable,related_name='thursday', on_delete=models.CASCADE, blank=True, null=True)
    friday = models.OneToOneField(DailyTimeTable,related_name='friday', on_delete=models.CASCADE, blank=True, null=True)
    saturday = models.OneToOneField(DailyTimeTable,related_name='saturday', on_delete=models.CASCADE, blank=True, null=True)
 
    def __str__(self):
        return f"{self.monday.period1._class}"