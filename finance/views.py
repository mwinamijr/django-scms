from rest_framework import generics, views, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter
import json

from academic.models import Teacher
from .models import Receipt, Payment
from .serializers import (ReceiptSerializer, PaymentSerializer)

class ReceiptsListView(views.APIView):
	"""
    List all Receipts, or create a new Receipt.
    """
	def get(self, request, format=None):
		receipts = Receipt.objects.all()
		serializer = ReceiptSerializer(receipts, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = ReceiptSerializer(data=request.data)
		print(request.data)
		print(serializer.is_valid())
		if serializer.is_valid():
			receipt = serializer.create(request)
			if receipt:
				#serializer.save()
				return Response(status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReceiptDetailView(views.APIView):
	def get_object(self, pk):
		try:
			return Receipt.objects.get(pk=pk)
		except Receipt.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		receipt = self.get_object(pk)
		serializer = ReceiptSerializer(receipt)
		return Response(serializer.data)
		
	def put(self, request, pk, format=None):
		receipt = self.get_object(pk)
		serializer = ReceiptSerializer(receipt, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		receipt = self.get_object(pk)
		receipt.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentListView(views.APIView):
	"""
    List all Payment, or create a new Payment.
    """
	def get(self, request, format=None):
		payments = Payment.objects.all()
		serializer = PaymentSerializer(payments, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = PaymentSerializer(data=request.data)
		print(request.data)
		print(serializer.is_valid())
		if serializer.is_valid():
			payment = serializer.create(request)
			if payment:
				#serializer.save()
				return Response(status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetailView(views.APIView):
	def get_object(self, pk):
		try:
			return Payment.objects.get(pk=pk)
		except Payment.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		payment = self.get_object(pk)
		serializer = PaymentSerializer(payment)
		return Response(serializer.data)
		
	def put(self, request, pk, format=None):
		payment = self.get_object(pk)
		serializer = PaymentSerializer(payment, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		payment = self.get_object(pk)
		payment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
