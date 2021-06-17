from django.urls import path
from notes.views import (
    NotesListView, ConceptListView, ConceptDetailView
)

urlpatterns = [
    path('notes-list/', NotesListView.as_view(), name="notes-list"),
    path('concepts-list/', ConceptListView.as_view(), name="concepts-list"),
    path('concepts-list/<int:pk>/', ConceptDetailView.as_view(), name="concept-detail"),
]
