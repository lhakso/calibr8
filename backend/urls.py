"""
URL configuration for backend project.

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
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import FileResponse
import os

def serve_frontend(request):
    """Serve the frontend index.html"""
    frontend_path = os.path.join(settings.BASE_DIR, 'frontend', 'index.html')
    return FileResponse(open(frontend_path, 'rb'), content_type='text/html')

urlpatterns = [
    path('', serve_frontend, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('predictions.urls')),
]

# Serve frontend static files
if settings.DEBUG:
    urlpatterns += static('/static/', document_root=os.path.join(settings.BASE_DIR, 'frontend', 'static'))
