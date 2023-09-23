from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
    
class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
