from rest_framework import serializers
from analyzer.models import ProcessedFile


class ProcessedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedFile
        fields = '__all__'

