# =====================================================================
# EJERCICIO 3: AUDITORÍA CON TESTS UNITARIOS E INTEGRACIÓN WEB
# EcoTech Solutions - Certificación de Huella de Carbono Industrial
# =====================================================================

import unittest

# --- 1. ALGORITMO PRINCIPAL DE CÁLCULO DE EMISIONES ---
def calcular_emisiones_carbono(consumo_kwh: float, factor_emision: float = 0.4) -> float:
    """
    Calcula las emisiones de CO2 industriales basadas en el consumo eléctrico (kWh).
    Eleva un ValueError si el consumo recibido es un valor negativo.
    """
    if consumo_kwh < 0:
        raise ValueError("El consumo en kWh no puede ser un valor negativo.")
    return float(consumo_kwh) * float(factor_emision)


# --- 2. PUNTO A: AUDITORÍA Y PRUEBAS AUTOMATIZADAS (UNITTEST) ---
class TestCalculoEmisiones(unittest.TestCase):
    """
    Clase de pruebas unitarias para certificar la precisión numérica 
    y la robustez ante errores del algoritmo de emisiones de carbono[cite: 3].
    """
    
    def test_calculo_emisiones_valido(self):
        """Verifica la exactitud matemática con valores nominales estándar (Factor 0.4)."""
        resultado = calcular_emisiones_carbono(1000, 0.4)
        self.assertEqual(resultado, 400.0)
        
    def test_calculo_emisiones_factor_personalizado(self):
        """Verifica el cálculo utilizando un factor de emisión diferente."""
        resultado = calcular_emisiones_carbono(500, 0.5)
        self.assertEqual(resultado, 250.0)

    def test_calculo_emisiones_consumo_negativo(self):
        """Verifica que se eleve correctamente la excepción ValueError ante consumos fuera de rango[cite: 3]."""
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-150, 0.4)


# --- 3. PUNTO B: PROCESAMIENTO DE MÉTRICAS Y VISTA DJANGO ---
def obtener_metricas_consumo(registros: list) -> dict:
    """
    Procesa un historial de registros de consumo por planta industrial[cite: 3]:
    Ejemplo: [{"planta": "Planta Norte", "consumo_kwh": 3400.0}, ...]
    Retorna un diccionario con el total global de emisiones y la planta de mayor consumo[cite: 3].
    """
    if not registros:
        return {
            "total_emisiones": 0.0,
            "planta_mayor_consumo": "Ninguna",
            "max_consumo_kwh": 0.0
        }
        
    total_emisiones = 0.0
    mayor_consumo = -1.0
    planta_critica = ""
    
    for reg in registros:
        planta = reg.get("planta", "Desconocida")
        consumo = reg.get("consumo_kwh", 0.0)
        
        # Calculamos las emisiones utilizando la función auditada
        emisiones = calcular_emisiones_carbono(consumo)
        total_emisiones += emisiones
        
        # Determinamos la planta con mayor requerimiento eléctrico
        if consumo > mayor_consumo:
            mayor_consumo = consumo
            planta_critica = planta
            
    return {
        "total_emisiones": round(total_emisiones, 2),
        "planta_mayor_consumo": planta_critica,
        "max_consumo_kwh": mayor_consumo
    }


# Integración con el framework Django (requiere entorno Django configurado en producción)
from django.shortcuts import render

def vista_panel_sustentabilidad(request):
    """
    Vista administrativa de Django que invoca el procesamiento analítico de métricas 
    y provee el diccionario de contexto listo para renderizar la plantilla 'sustentabilidad/panel.html'[cite: 3].
    """
    # Historial simulado de consumo eléctrico de las plantas de EcoTech Solutions
    historial_plantas = [
        {"planta": "Planta Norte", "consumo_kwh": 3400.0},
        {"planta": "Planta Sur", "consumo_kwh": 5100.0},
        {"planta": "Planta Este", "consumo_kwh": 2150.0},
        {"planta": "Planta Oeste", "consumo_kwh": 1800.0}
    ]
    
    # Procesar métricas utilizando la tubería analítica
    metricas = obtener_metricas_consumo(historial_plantas)
    
    # Construir el diccionario de contexto para la plantilla HTML
    contexto = {
        'titulo_panel': 'Panel de Control de Sostenibilidad - EcoTech',
        'total_emisiones_co2': metricas['total_emisiones'],
        'planta_critica': metricas['planta_mayor_consumo'],
        'max_consumo_kwh': metricas['max_consumo_kwh'],
        'registros_plantas': historial_plantas
    }
    
    # Retorna la renderización hacia la plantilla especificada
    return render(request, 'sustentabilidad/panel.html', contexto)


# =====================================================================
# BLOQUE DE EJECUCIÓN DE PRUEBAS UNITARIAS (COMPATIBLE CON COLAB)
# =====================================================================
if __name__ == "__main__":
    print("=== INICIANDO AUDITORÍA DE EMISIONES DE CARBONO (UNITTEST) ===")
    # Ejecutamos las pruebas unitarias adaptadas para entornos interactivos o notebooks
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
#```[cite: 3]

#---

### **Resumen de la Implementación del Ejercicio 3**
#1. **Auditoría Automatizada (`TestCalculoEmisiones`):** Verifica con precisión matemática que el factor de emisión estándar (`0.4`) entregue los valores esperados y comprueba que se dispare de forma controlada el error `ValueError` ante valores de consumo negativos[cite: 3].
#2. **Tubería Analítica (`obtener_metricas_consumo`):** Agrega y procesa de manera automática los registros históricos de consumo de las plantas industriales de EcoTech Solutions para aislar la planta crítica con mayor demanda energética[cite: 3].
#3. **Integración Web (`vista_panel_sustentabilidad`):** Conecta la lógica de negocio directamente con la arquitectura del framework Django a través del diccionario de contexto requerido por la plantilla institucional `sustentabilidad/panel.html`[cite: 3].