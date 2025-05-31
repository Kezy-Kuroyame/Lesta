import os
from django.http import JsonResponse
from system.metrics import metrics

def status_view(request):
    return JsonResponse({"status": "OK"})


def version_view(request):
    version = os.environ.get("APP_VERSION", "0.1.0")
    return JsonResponse({"version": version})


def metrics_view(request):
    return JsonResponse(metrics.get_metrics())