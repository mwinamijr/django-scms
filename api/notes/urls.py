from django.urls import path
from notes.views import (
    NotesListView
)

urlpatterns = [
    path('notes-list/', NotesListView.as_view(), name="notes-list"),
]
