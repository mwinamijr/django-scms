from django.db import models
import httpagentparser

class Subject(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    short_name = models.CharField(max_length=5, blank=True, null=True)

    def __str_(self):
        return self.name

class Period(models.Model):
    name = models.OneToOneField(Subject, related_name='period')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ('start_time',)

    def __str__(self):
        return "%s %s-%s" % (self.name, self.start_time.strftime('%I:%M%p'), self.end_time.strftime('%I:%M%p'))


class DailyTimeTable(models.Model):
    period1 = models.OneToOneField(Period,related_name='period1')
    period2 = models.OneToOneField(Period,related_name='period2')
    period3 = models.OneToOneField(Period,related_name='period3')
    period4 = models.OneToOneField(Period,related_name='period4')
    period5 = models.OneToOneField(Period,related_name='period5')
    period6 = models.OneToOneField(Period,related_name='period6')
    period7 = models.OneToOneField(Period,related_name='period7')
    period8 = models.OneToOneField(Period,related_name='period8')


class WeeklyTimeTable(models.Model):
    monday = models.OneToOneField(DailyTimeTable,related_name='monday')
    tuesday = models.OneToOneField(DailyTimeTable,related_name='tuesday')
    wednesday = models.OneToOneField(DailyTimeTable,related_name='wednesday')
    thursday = models.OneToOneField(DailyTimeTable,related_name='thursday')
    friday = models.OneToOneField(DailyTimeTable,related_name='friday')
    saturday = models.OneToOneField(DailyTimeTable,related_name='saturday')
 

class ClassTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    class_section = models.ForeignKey('ClassSection', on_delete=models.CASCADE, blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher', 'class_section')

class ClassSection(models.Model):
    classLevel = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, blank=True, null=True)
    section = models.CharField(max_length=1, choices=(('A', 'A'), ('B', 'B'),('C', 'C')))
    students = models.ManyToManyField('sis.Student', blank=True)
    year = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.classLevel} {self.section}"
