from rest_framework import serializers

from .models import *

class ClassJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassJournal
        fields = "__all__"

