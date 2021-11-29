from rest_framework import serializers

from .models import *
from sis.serializers import StudentSerializer
from users.serializers import AccountantSerializer

class AllocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Allocation
        fields = "__all__"

class ReceiptSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(read_only=True)
    paid_for = serializers.SerializerMethodField(read_only=True)
    received_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Receipt
        fields = "__all__"
    
    def get_student(self, obj):
        student = obj.student
        serializer = StudentSerializer(student, many=False)
        student = serializer.data['fname'] + " " + serializer.data['lname']
        return student
    
    def get_paid_for(self, obj):
        paid_for = obj.paid_for
        serializer = AllocationSerializer(paid_for, many=False)
        paid_for = serializer.data['name']
        return paid_for

    def get_received_by(self, obj):
        received_by = obj.received_by
        serializer = AccountantSerializer(received_by, many=False)
        received_by = serializer.data['user']

        return received_by


