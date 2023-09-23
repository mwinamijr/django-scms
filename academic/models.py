from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    order_rank = models.IntegerField(blank=True, null=True, help_text="Rank that courses will show up in reports")

    class Meta:
        ordering = ('order_rank', 'name')

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subject_code = models.CharField(max_length=10, blank=True, null=True, unique=True)
    is_selectable = models.BooleanField(default=False, help_text="select if subject is optional")
    graded = models.BooleanField(default=True, help_text='Teachers can submit grades for this course')
    description = models.CharField(max_length=255, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True,
                                   help_text="the department associated with this subject")

    def __str__(self):
        return self.name
