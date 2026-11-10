# Ejercicio 1: Sanitización y Análisis Estadístico de Sensores

Este módulo forma parte del proyecto final de **EcoTech Solutions** para el curso FESaT. Su propósito principal es procesar lecturas térmicas heterogéneas transmitidas por microcontroladores industriales, limpiando anomalías de formato y generando un reporte consolidado para la toma de decisiones[cite: 3, 4].

---

## 📋 Descripción de la Consigna

Los microcontroladores de campo suelen enviar datos crudos que contienen espacios indeseados, textos combinados con unidades de medida y atributos incompletos. El sistema resuelve este problema mediante dos funciones clave[cite: 4]:

1. **Punto A (`limpiar_registro_sensor`):** 
   Procesa diccionarios individuales con datos crudos (ej. `{"sensor_id": " Sensor-001 ", "temperatura": "24.5 ºC", "ubicación": "Planta Norte"}`)[cite: 4].
   * Normaliza el identificador eliminando espacios excedentes[cite: 4].
   * Limpia y convierte la temperatura a un formato numérico flotante (`float`), removiendo sufijos heterogéneos de unidades (`ºC`, `°C`, `ºc`, `°c`, `C`, `c`, `º`, `˚`, `⁰`)[cite: 4].
   * Asigna un valor de ubicación por defecto seguro en caso de que el campo esté vacío, nulo o ausente[cite: 4].

2. **Punto B (`generar_resumen_sensores`):** 
   Toma la colección de registros ya sanitizados y un umbral límite de temperatura configurable[cite: 4].
   * Retorna una tupla que contiene la lista de identificadores de los dispositivos que superan el umbral estipulado y el promedio térmico global de la planta[cite: 4].

---

## 💻 Código Fuente (`main.py`)

```python
# =====================================================================
# EJERCICIO 1: SANITIZACIÓN Y ANÁLISIS ESTADÍSTICO DE SENSORES
# EcoTech Solutions - Monitoreo de microcontroladores térmicos
# =====================================================================

def limpiar_registro_sensor(registro_raw: dict, ubicacion_defecto: str = "Planta General") -> dict:
    """
    Normaliza el registro crudo de un sensor:
    - Elimina espacios en el identificador.
    - Remueve sufijos de unidades térmicas heterogéneas.
    - Asigna una ubicación por defecto en caso de estar ausente o vacía.
    """
    sensor_id_raw = registro_raw.get("sensor_id", "Sensor-Desconocido")
    sensor_id = str(sensor_id_raw).strip()
    
    temp_raw = registro_raw.get("temperatura")
    if temp_raw is None:
        temperatura = 0.0
    elif isinstance(temp_raw, (int, float)):
        temperatura = float(temp_raw)
    else:
        temp_str = str(temp_raw)
        sufijos_unidades = ["ºC", "°C", "ºc", "°c", "C", "c", "º", "˚", "⁰"]
        for sufijo in sufijos_unidades:
            temp_str = temp_str.replace(sufijo, "")
        temp_str = temp_str.strip()
        
        try:
            temperatura = float(temp_str)
        except ValueError:
            temperatura = 0.0

    ubicacion_raw = registro_raw.get("ubicación")
    if ubicacion_raw is None or str(ubicacion_raw).strip() == "":
        ubicacion = ubicacion_defecto
    else:
        ubicacion = str(ubicacion_raw).strip()
        
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicación": ubicacion
    }


def generar_resumen_sensores(lista_sensores_limpios: list, umbral_temperatura: float) -> tuple:
    """
    Calcula la lista de sensores que superan el umbral estipulado
    y el promedio térmico global de la planta.
    """
    if not lista_sensores_limpios:
        return [], 0.0
        
    lista_sensores_alerta = [
        sensor["sensor_id"] for sensor in lista_sensores_limpios 
        if sensor["temperatura"] > umbral_temperatura
    ]
    
    suma_temperaturas = sum(sensor["temperatura"] for sensor in lista_sensores_limpios)
    promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    
    return lista_sensores_alerta, promedio_temperatura


# =====================================================================
# BLOQUE DE EJECUCIÓN E INTERACCIÓN
# =====================================================================
if __name__ == "__main__":
    print("=== SISTEMA DE MONITOREO DE SENSORES - ECOTECH SOLUTIONS ===\n")
    
    ubicacion_default = "Planta General"
    umbral_limite = 28.0

    # Registros crudos de prueba con datos heterogéneos y espacios
    registros_crudos = [
        {"sensor_id": " Sensor-001 ", "temperatura": "24.5 ºC", "ubicación": "Planta Norte"},
        {"sensor_id": "Sensor-002", "temperatura": "29.8 °c", "ubicación": ""},
        {"sensor_id": " Sensor-003 ", "temperatura": "31⁰", "ubicación": "   "},
        {"sensor_id": "Sensor-004", "temperatura": " 22 ˚ ", "ubicación": None},
        {"sensor_id": "Sensor-005", "temperatura": "35.2 C", "ubicación": "Planta Sur"}
    ]

    sensores_limpios = [
        limpiar_registro_sensor(reg, ubicacion_defecto=ubicacion_default) 
        for reg in registros_crudos
    ]

    print("[RESULTADO] Registros Sanitizados:")
    for s in sensores_limpios:
        print(f"  -> ID: {s['sensor_id']} | Temp: {s['temperatura']} ºC | Ubicación: {s['ubicación']}")

    alertas, promedio = generar_resumen_sensores(sensores_limpios, umbral_temperatura=umbral_limite)

    print(f"\n[REPORTE ESTADÍSTICO] (Umbral: {umbral_limite} ºC):")
    print(f"   • Promedio térmico global: {promedio:.2f} ºC")
    print(f"   • Dispositivos en alerta: {alertas}")