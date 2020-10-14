from django.db import models

CLASS_CHOICES = [
	('Form One', 'Form One'),
	('Form Two', 'Form Two'),
	('Form Three', 'Form Three'),
	('Form Four', 'Form Four'),
]

RELIGION_CHOICES = [
	('Muslim', 'Muslim'),
	('Christian', 'Christian'),
]

class Student(models.Model):
	firstName = models.CharField(max_length=20, blank=True, null=True)
	middleName = models.CharField(max_length=20, blank=True, null=True)
	lastName = models.CharField(max_length=20, blank=True, null=True)
	birthDate = models.DateField(auto_now_add=False)
	religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, default='Muslim', blank=True, null=True)
	parentPhone = models.CharField(max_length=12, blank=True, null=True)
	classLevel = models.CharField(max_length=10, choices=CLASS_CHOICES, blank=True, null=True)
	stream = models.CharField(max_length=1, blank=True, null=True)

	def __str__(self):
		return f"{self.firstName} {self.middleName} {self.lastName} "