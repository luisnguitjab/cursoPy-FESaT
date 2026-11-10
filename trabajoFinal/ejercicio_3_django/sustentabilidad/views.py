"""
Vistas y Lógica de Negocio de Sustentabilidad - EcoTech Solutions
"""
from django.shortcuts import render


def calcular_emisiones_carbono(consumo_kwh: float, factor_emision: float = 0.4) -> float:
    """
    Calcula las emisiones de CO2 industriales basadas en el consumo eléctrico (kWh).
    Eleva un ValueError si el consumo recibido es un valor negativo.
    """
    if consumo_kwh < 0:
        raise ValueError("El consumo en kWh no puede ser un valor negativo.")
    return float(consumo_kwh) * float(factor_emision)


def obtener_metricas_consumo(registros: list) -> dict:
    """
    Procesa un historial de registros de consumo por planta industrial.
    Retorna el total de emisiones y la planta con mayor consumo eléctrico.
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


def vista_panel_sustentabilidad(request):
    """
    Vista administrativa que alimenta el panel de control ambiental.
    """
    historial_plantas = [
        {"planta": "Planta Norte", "consumo_kwh": 3400.0},
        {"planta": "Planta Sur", "consumo_kwh": 5100.0},
        {"planta": "Planta Este", "consumo_kwh": 2150.0},
        {"planta": "Planta Oeste", "consumo_kwh": 1800.0}
    ]

    metricas = obtener_metricas_consumo(historial_plantas)

    contexto = {
        'titulo_panel': 'Panel de Control de Sostenibilidad - EcoTech Solutions',
        'total_emisiones_co2': metricas['total_emisiones'],
        'planta_critica': metricas['planta_mayor_consumo'],
        'max_consumo_kwh': metricas['max_consumo_kwh'],
        'registros_plantas': historial_plantas
    }

    return render(request, 'sustentabilidad/panel.html', contexto)
