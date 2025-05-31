"""
URL configuration for text_analyzer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from analyzer.views import analyze_text
from text_analyzer import settings
from analyzer.views import handle_get_request
from system import endpoints


urlpatterns = [
    path("status", endpoints.status_view),
    path("version", endpoints.version_view),
    path("metrics", endpoints.metrics_view),
    path('admin/', admin.site.urls),
    path('', analyze_text, name='analyze'),
    path('results/', handle_get_request, name='results'),
]