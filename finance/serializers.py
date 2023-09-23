from rest_framework import serializers

from .models import *
from academic.models import Student
from users.models import CustomUser
from academic.serializers import StudentSerializer
from users.serializers import AccountantSerializer, UserSerializer

class ReceiptAllocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReceiptAllocation
        fields = "__all__"

class PaymentAllocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PaymentAllocation
        fields = "__all__"

class ReceiptSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    paid_for = serializers.SerializerMethodField()
    received_by = serializers.SerializerMethodField()

    class Meta:
        model = Receipt
        fields = ('id', 'receipt_no', 'date', 'student', 'paid_for', 'payer', 'amount', 'received_by')
    
    def get_student(self, obj):
        student = obj.student
        serializer = StudentSerializer(student, many=False)
        student = serializer.data['first_name'] + " " + serializer.data['last_name']
        return student
    
    def get_paid_for(self, obj):
        paid_for = obj.paid_for
        serializer = ReceiptAllocationSerializer(paid_for, many=False)
        paid_for = serializer.data['name']
        return paid_for

    def get_received_by(self, obj):
        received_by = obj.received_by
        serializer = AccountantSerializer(received_by, many=False)
        received_by = serializer.data['user']
        return received_by

    def create(self, request):
        data= request.data
        receipt = Receipt()
        receipt.receipt_no = data['receipt_no']
        student = Student.objects.get(first_name=data['student'])
        paid_for = ReceiptAllocation.objects.get(name=data['paid_for'])
        received_by = Accountant.objects.get(user=CustomUser.objects.get(first_name=data['received_by']))
        receipt.payer = data['payer']
        receipt.amount = data['amount']
        receipt.student = student
        receipt.paid_for = paid_for
        receipt.received_by = received_by
        receipt.save()
        return receipt 

class PaymentSerializer(serializers.ModelSerializer):
    paid_for = serializers.SerializerMethodField(read_only=True)
    paid_by = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"
    
    def get_paid_for(self, obj):
        paid_for = obj.paid_for
        serializer = PaymentAllocationSerializer(paid_for, many=False)
        paid_for = serializer.data['name']
        return paid_for

    def get_paid_by(self, obj):
        paid_by = obj.paid_by
        serializer = AccountantSerializer(paid_by, many=False)
        paid_by = serializer.data['user']

        return paid_by

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        user = serializer.data['first_name']
        return user

    def create(self, request):
        data= request.data
        payment = Payment()
        payment.payment_no = data['payment_no']
        paid_for = PaymentAllocation.objects.get(name=data['paid_for'])
        paid_by = Accountant.objects.get(user=CustomUser.objects.get(first_name=data['paid_by']))
        payment.paid_to = data['paid_to']
        payment.amount = data['amount']
        payment.paid_for = paid_for
        payment.paid_by = paid_by
        payment.save()
        return payment
