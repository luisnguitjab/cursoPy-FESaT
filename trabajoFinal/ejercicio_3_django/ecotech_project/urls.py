"""
URL Configuration for ecotech_project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sustentabilidad/', include('sustentabilidad.urls')),
    path('', include('sustentabilidad.urls')),  # Ruta raíz redirigida al panel de sustentabilidad
]
