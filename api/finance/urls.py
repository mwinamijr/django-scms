from django.urls import path, include
from rest_framework.routers import DefaultRouter
from finance.views import (
	ReceiptsListView, ReceiptDetailView,
    )


urlpatterns = [
	path('receipts/', ReceiptsListView.as_view(), name="receipt-list"),
    path('receipts/<int:pk>/', ReceiptDetailView.as_view(), name="receipt-detail"),
]