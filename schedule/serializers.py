from rest_framework import serializers

from .models import *

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = "__all__"

class DailyTimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTimeTable
        fields = "__all__"

class WeeklyTimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyTimeTable
        fields = "__all__"