import os

from django.db.models import Min, Max
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from system.serializers import ProcessedFileSerializer
from analyzer.models import ProcessedFile


def status_view(request):
    return JsonResponse({"status": "OK"})


def version_view(request):
    version = os.environ.get("APP_VERSION", "0.1.0")
    return JsonResponse({"version": version})


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def metrics_view(request):
    file_count = ProcessedFile.objects.count()
    latest_file = ProcessedFile.objects.order_by('-processed_at').first()
    min_time = ProcessedFile.objects.aggregate(Min("processing_time"))["processing_time__min"]
    max_time = ProcessedFile.objects.aggregate(Max("processing_time"))["processing_time__max"]

    files_python = ProcessedFile.objects.all()
    files_json = ProcessedFileSerializer(files_python, many=True).data
    data = {
        "metrics": {
            "total_files": file_count,
            "latest_file": latest_file.filename if latest_file else None,
            "min_processing_time": float(min_time) if min_time else None,
            "max_processing_time": float(max_time) if max_time else None,
        },
        "files": files_json
    }
    return Response(data)

