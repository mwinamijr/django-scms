from django.db import models
import httpagentparser

from users.models import Teacher

class Subject(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    short_name = models.CharField(max_length=5, blank=True, null=True)

    def __str_(self):
        return self.name

class Period(models.Model):
    name = models.OneToOneField(Subject, related_name='period', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ('start_time',)

    def __str__(self):
        return "%s %s-%s" % (self.name, self.start_time.strftime('%I:%M%p'), self.end_time.strftime('%I:%M%p'))


class DailyTimeTable(models.Model):
    period1 = models.OneToOneField(Period,related_name='period1', on_delete=models.CASCADE)
    period2 = models.OneToOneField(Period,related_name='period2', on_delete=models.CASCADE)
    period3 = models.OneToOneField(Period,related_name='period3', on_delete=models.CASCADE)
    period4 = models.OneToOneField(Period,related_name='period4', on_delete=models.CASCADE)
    period5 = models.OneToOneField(Period,related_name='period5', on_delete=models.CASCADE)
    period6 = models.OneToOneField(Period,related_name='period6', on_delete=models.CASCADE)
    period7 = models.OneToOneField(Period,related_name='period7', on_delete=models.CASCADE)
    period8 = models.OneToOneField(Period,related_name='period8', on_delete=models.CASCADE)


class WeeklyTimeTable(models.Model):
    monday = models.OneToOneField(DailyTimeTable,related_name='monday', on_delete=models.CASCADE)
    tuesday = models.OneToOneField(DailyTimeTable,related_name='tuesday', on_delete=models.CASCADE)
    wednesday = models.OneToOneField(DailyTimeTable,related_name='wednesday', on_delete=models.CASCADE)
    thursday = models.OneToOneField(DailyTimeTable,related_name='thursday', on_delete=models.CASCADE)
    friday = models.OneToOneField(DailyTimeTable,related_name='friday', on_delete=models.CASCADE)
    saturday = models.OneToOneField(DailyTimeTable,related_name='saturday', on_delete=models.CASCADE)
 
