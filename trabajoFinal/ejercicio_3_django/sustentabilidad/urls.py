"""
Enrutador interno de URLs para la aplicación sustentabilidad.
"""
from django.urls import path
from .views import vista_panel_sustentabilidad

urlpatterns = [
    path('', vista_panel_sustentabilidad, name='panel_sustentabilidad'),
]
