from django.db import models
from django.conf import settings
from datetime import date

class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to='api/sis/students/bulkupload')

