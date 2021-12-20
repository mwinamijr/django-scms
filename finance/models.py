from django.db import models

from sis.models import Student
from users.models import Accountant

class Allocation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class PaymentAllocation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Receipt(models.Model):
    receipt_no = models.IntegerField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    payer = models.CharField(max_length=255, null=True)
    paid_for = models.ForeignKey(Allocation,  on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(Student,  on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()
    received_by = models.ForeignKey(Accountant, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.paid_for} - {self.date} - {self.payer}"

class Payment(models.Model):
    payment_no = models.IntegerField(unique=True)
    date = models.DateField(auto_now_add=True)
    paid_to = models.CharField(max_length=255, blank=True, null=True)
    paid_for = models.ForeignKey(PaymentAllocation,  on_delete=models.DO_NOTHING)
    amount = models.IntegerField()
    paid_by = models.ForeignKey(Accountant, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.paid_for} - {self.date} - {self.payer}"
