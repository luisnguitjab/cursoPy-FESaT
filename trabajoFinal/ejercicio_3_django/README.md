# Ejercicio 3: Auditoría con Pruebas Unitarias e Integración Web en Django

Este módulo forma parte del proyecto final de **EcoTech Solutions** para el curso FESaT. Su objetivo es auditar mediante pruebas automatizadas el algoritmo de cálculo de huella de carbono industrial de la empresa e integrarlo en una vista administrativa de **Django** para la visualización del panel de sostenibilidad.

---

## Descripción de la Consigna

El ejercicio consta de dos secciones fundamentales:

1. **Punto A (`TestCalculoEmisiones`):**
   * Definición de la función `calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4)`.
   * Validación de negocio: Lanza una excepción `ValueError` si el consumo en kWh es un número negativo.
   * Auditoría automatizada con `unittest`: Suite de pruebas que certifica la exactitud del cálculo nominal (factor 0.4 y personalizados) y la correcta captura de la excepción ante consumos inválidos.

2. **Punto B (`obtener_metricas_consumo` y Vista Django):**
   * Función `obtener_metricas_consumo(registros)`: Procesa un listado de plantas industriales, calcula el total acumulado de emisiones de CO2 y detecta la planta con mayor consumo energético.
   * Vista de Django (`vista_panel_sustentabilidad`): Recibe las solicitudes HTTP, invoca el pipeline de métricas y renderiza la plantilla `sustentabilidad/panel.html` enviando el diccionario de contexto.

---

## Estructura del Proyecto Django

```text
ejercicio_3_django/
├── ecotech_project/          # Carpeta de configuración global de Django
│   ├── __init__.py
│   ├── settings.py           # Configuración del proyecto y APPS instaladas
│   ├── urls.py               # Enrutador principal de URLs
│   ├── wsgi.py
│   └── asgi.py
├── sustentabilidad/          # Aplicación de Django para el panel ambiental
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py              # Suite de pruebas unitarias (TestCalculoEmisiones)
│   ├── views.py              # Vista administrativa (vista_panel_sustentabilidad)
│   ├── urls.py               # Rutas internas de la aplicación
│   └── templates/
│       └── sustentabilidad/
│           └── panel.html    # Plantilla HTML del panel de control
├── manage.py                 # Script de gestión de comandos de Django
├── requirements.txt          # Dependencias del proyecto (Django)
└── README.md                 # Documentación del ejercicio
```

---

## Código de la Vista e Integración (`views.py`)

```python
import unittest
from django.shortcuts import render

# 1. ALGORITMO PRINCIPAL DE CÁLCULO DE EMISIONES
def calcular_emisiones_carbono(consumo_kwh: float, factor_emision: float = 0.4) -> float:
    """Calcula emisiones de CO2. Eleva ValueError si el consumo es negativo."""
    if consumo_kwh < 0:
        raise ValueError("El consumo en kWh no puede ser un valor negativo.")
    return float(consumo_kwh) * float(factor_emision)


# 2. PROCESAMIENTO DE MÉTRICAS GLOBALES
def obtener_metricas_consumo(registros: list) -> dict:
    """Procesa la lista de plantas y devuelve emisiones totales y planta crítica."""
    if not registros:
        return {"total_emisiones": 0.0, "planta_mayor_consumo": "Ninguna", "max_consumo_kwh": 0.0}
        
    total_emisiones = 0.0
    mayor_consumo = -1.0
    planta_critica = ""
    
    for reg in registros:
        planta = reg.get("planta", "Desconocida")
        consumo = reg.get("consumo_kwh", 0.0)
        
        emisiones = calcular_emisiones_carbono(consumo)
        total_emisiones += emisiones
        
        if consumo > mayor_consumo:
            mayor_consumo = consumo
            planta_critica = planta
            
    return {
        "total_emisiones": round(total_emisiones, 2),
        "planta_mayor_consumo": planta_critica,
        "max_consumo_kwh": mayor_consumo
    }


# 3. VISTA ADMINISTRATIVA DE DJANGO
def vista_panel_sustentabilidad(request):
    """Renderiza el panel de sostenibilidad ambiental en 'sustentabilidad/panel.html'."""
    historial_plantas = [
        {"planta": "Planta Norte", "consumo_kwh": 3400.0},
        {"planta": "Planta Sur", "consumo_kwh": 5100.0},
        {"planta": "Planta Este", "consumo_kwh": 2150.0},
        {"planta": "Planta Oeste", "consumo_kwh": 1800.0}
    ]
    
    metricas = obtener_metricas_consumo(historial_plantas)
    
    contexto = {
        'titulo_panel': 'Panel de Control de Sostenibilidad - EcoTech',
        'total_emisiones_co2': metricas['total_emisiones'],
        'planta_critica': metricas['planta_mayor_consumo'],
        'max_consumo_kwh': metricas['max_consumo_kwh'],
        'registros_plantas': historial_plantas
    }
    
    return render(request, 'sustentabilidad/panel.html', contexto)

---

## Pruebas Unitarias (`tests.py`)

Para ejecutar la suite de pruebas automatizadas y certificar la calidad del algoritmo en Django, corre el siguiente comando en la terminal:

python manage.py test sustentabilidad


El código del test verifica tanto casos válidos como la captura del error `ValueError`:

```python
class TestCalculoEmisiones(unittest.TestCase):
    def test_calculo_emisiones_valido(self):
        self.assertEqual(calcular_emisiones_carbono(1000, 0.4), 400.0)
        
    def test_calculo_emisiones_factor_personalizado(self):
        self.assertEqual(calcular_emisiones_carbono(500, 0.5), 250.0)

    def test_calculo_emisiones_consumo_negativo(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-150, 0.4)
```

---

## Instrucciones para Levantar el Servidor Django

1. Situarse en la carpeta del ejercicio 3:
   
   cd ejercicio_3_django/
   
2. Instalar las dependencias necesarias:
   
   pip install -r requirements.txt
   
3. Ejecutar las migraciones base de Django:
   
   python manage.py migrate
   
4. Iniciar el servidor de desarrollo local:
   
   python manage.py runserver
   
5. Acceder desde el navegador web a:
   `http://127.0.0.1:8000/sustentabilidad/`
