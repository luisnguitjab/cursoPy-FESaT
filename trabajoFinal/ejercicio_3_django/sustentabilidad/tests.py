"""
Suite de Pruebas Unitarias - EcoTech Solutions (Ejercicio 3)
Auditoría del algoritmo de huella de carbono industrial.
"""
import unittest
from django.test import TestCase
from sustentabilidad.views import calcular_emisiones_carbono, obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    """
    Suite de pruebas unitarias para validar el comportamiento del algoritmo
    de cálculo de emisiones de carbono y captura de excepciones.
    """

    def test_calculo_emisiones_valido(self):
        """Prueba con consumo nominal y factor de emisión por defecto (0.4)."""
        resultado = calcular_emisiones_carbono(1000.0, 0.4)
        self.assertEqual(resultado, 400.0)

    def test_calculo_emisiones_factor_personalizado(self):
        """Prueba con un factor de emisión distinto."""
        resultado = calcular_emisiones_carbono(500.0, 0.5)
        self.assertEqual(resultado, 250.0)

    def test_calculo_emisiones_consumo_negativo(self):
        """Verifica que se eleve la excepción ValueError ante consumo negativo."""
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-150.0, 0.4)


class TestMetricasConsumo(unittest.TestCase):
    """
    Pruebas unitarias para la agregación de métricas de plantas industriales.
    """

    def test_obtener_metricas_historial(self):
        datos = [
            {"planta": "Planta Norte", "consumo_kwh": 1000.0},
            {"planta": "Planta Sur", "consumo_kwh": 2000.0}
        ]
        metricas = obtener_metricas_consumo(datos)
        # 1000*0.4 + 2000*0.4 = 400 + 800 = 1200
        self.assertEqual(metricas["total_emisiones"], 1200.0)
        self.assertEqual(metricas["planta_mayor_consumo"], "Planta Sur")
        self.assertEqual(metricas["max_consumo_kwh"], 2000.0)

    def test_obtener_metricas_vacio(self):
        metricas = obtener_metricas_consumo([])
        self.assertEqual(metricas["total_emisiones"], 0.0)
        self.assertEqual(metricas["planta_mayor_consumo"], "Ninguna")
