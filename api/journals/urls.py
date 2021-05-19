from django.urls import path, include
from rest_framework.routers import DefaultRouter
from administration.views import (
	ClassJournalListView, ClassJournalDetailView,
    )


urlpatterns = [
	path('class-journals/', ClassJournalListView.as_view(), name="class-journals-list"),
    path('class-journals/<int:pk>/', ClassJournalDetailView.as_view(), name="class-journals-detail"),
]