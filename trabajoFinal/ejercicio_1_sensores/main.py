# =====================================================================
# EJERCICIO 1: SANITIZACIÓN Y ANÁLISIS ESTADÍSTICO DE SENSORES
# EcoTech Solutions - Monitoreo de microcontroladores térmicos
# =====================================================================

def limpiar_registro_sensor(registro_raw: dict, ubicacion_defecto: str = "Planta General") -> dict:
    """
    Punto A: Normalización de lecturas individuales (limpiar_registro_sensor).
    Toma un diccionario con datos crudos de un sensor y retorna un nuevo 
    diccionario estandarizado, eliminando espacios, limpiando sufijos de unidades 
    y aplicando un valor por defecto seguro para la ubicación si está vacía.
    """
    # 1. Obtenemos el ID crudo del sensor; si no existe, asignamos una etiqueta genérica
    sensor_id_raw = registro_raw.get("sensor_id", "Sensor-Desconocido")
    
    # 2. Eliminamos los espacios en blanco sobrantes al inicio y final del ID
    sensor_id = str(sensor_id_raw).strip()
    
    # 3. Obtenemos el valor de la temperatura cruda
    temp_raw = registro_raw.get("temperatura")
    
    # 4. Verificamos si la temperatura es nula (None) para manejarla de manera segura
    if temp_raw is None:
        temperatura = 0.0
    # 5. Si ya es un valor numérico (int o float), lo convertimos directamente a float
    elif isinstance(temp_raw, (int, float)):
        temperatura = float(temp_raw)
    else:
        # 6. Si es una cadena de texto, la convertimos para proceder a remover sufijos
        temp_str = str(temp_raw)
        
        # 7. Definimos la lista exhaustiva de sufijos de unidad de temperatura a limpiar
        sufijos_unidades = ["ºC", "°C", "ºc", "°c", "C", "c", "º", "˚", "⁰"]
        
        # 8. Recorremos cada sufijo y lo reemplazamos por una cadena vacía en el texto
        for sufijo in sufijos_unidades:
            temp_str = temp_str.replace(sufijo, "")
            
        # 9. Limpiamos los espacios en blanco que puedan haber quedado alrededor del número
        temp_str = temp_str.strip()
        
        # 10. Intentamos convertir la cadena resultante a número decimal (float)
        try:
            temperatura = float(temp_str)
        except ValueError:
            # 11. Si ocurre un error de formato no reconocido, asignamos un valor por defecto seguro
            temperatura = 0.0

    # 12. Obtenemos el valor de la ubicación del registro crudo
    ubicacion_raw = registro_raw.get("ubicación")
    
    # 13. Evaluamos si la ubicación está ausente, es None o está compuesta solo por espacios
    if ubicacion_raw is None or str(ubicacion_raw).strip() == "":
        ubicacion = ubicacion_defecto  # Se aplica el valor por defecto seguro
    else:
        # 14. Si contiene información válida, se eliminan los espacios sobrantes
        ubicacion = str(ubicacion_raw).strip()
        
    # 15. Retornamos el diccionario sanitizado y estructurado con claves estándar
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicación": ubicacion
    }


def generar_resumen_sensores(lista_sensores_limpios: list, umbral_temperatura: float) -> tuple:
    """
    Punto B: Monitoreo y mapeo estadístico (generar_resumen_sensores).
    Toma una colección de registros sanitizados y un valor límite. Retorna una 
    tupla (lista_sensores_alerta, promedio_temperatura) con los IDs de los 
    dispositivos que superan el umbral y el promedio térmico global de la planta[cite: 3].
    """
    # 1. Validamos si la lista recibida está vacía para evitar errores de división por cero
    if not lista_sensores_limpios:
        return [], 0.0
        
    # 2. Filtramos mediante list comprehension los IDs de los sensores que superan el umbral estipulado
    lista_sensores_alerta = [
        sensor["sensor_id"] for sensor in lista_sensores_limpios 
        if sensor["temperatura"] > umbral_temperatura
    ]
    
    # 3. Sumamos el total de las temperaturas de todos los dispositivos sanitizados
    suma_temperaturas = sum(sensor["temperatura"] for sensor in lista_sensores_limpios)
    
    # 4. Calculamos el promedio térmico global dividiendo la suma entre la cantidad de registros
    promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    
    # 5. Retornamos la tupla consolidada con los resultados del monitoreo
    return lista_sensores_alerta, promedio_temperatura


# =====================================================================
# BLOQUE DE EJECUCIÓN (DEMOSTRACIÓN DEL FLUJO COMPLETO)
# =====================================================================
if __name__ == "__main__":
    print("=== SISTEMA DE MONITOREO DE SENSORES - ECOTECH SOLUTIONS ===\n")
    
    # 1. Solicitamos la configuración de parámetros iniciales
    input_ub = input("Ingrese la ubicación por defecto para campos vacíos [Enter para 'Planta General']: ").strip()
    ubicacion_default = input_ub if input_ub != "" else "Planta General"
    
    input_umbral = input("Ingrese el umbral de temperatura límite (ºC) [Enter para 28.0]: ").strip()
    try:
        umbral_limite = float(input_umbral) if input_umbral != "" else 28.0
    except ValueError:
        print("Valor inválido ingresado. Se utilizará por defecto el umbral de 28.0 ºC.")
        umbral_limite = 28.0

    print("\n--- INGRESO DE DATOS CRUDOS DE PRUEBA ---")
    
    # 2. Definimos un conjunto de registros crudos simulando la heterogeneidad de los microcontroladores
    registros_crudos = [
        {"sensor_id": " Sensor-001 ", "temperatura": "24.5 ºC", "ubicación": "Planta Norte"},
        {"sensor_id": "Sensor-002", "temperatura": "29.8 °c", "ubicación": ""},           # Ubicación vacía
        {"sensor_id": " Sensor-003 ", "temperatura": "31⁰", "ubicación": "   "},           # Espacios en ubicación
        {"sensor_id": "Sensor-004", "temperatura": " 22 ˚ ", "ubicación": None},          # Ubicación None
        {"sensor_id": "Sensor-005", "temperatura": "35.2 C", "ubicación": "Planta Sur"}
    ]

    # 3. Procesamos y sanitizamos la colección completa aplicando la función del Punto A
    sensores_limpios = [
        limpiar_registro_sensor(reg, ubicacion_defecto=ubicacion_default) 
        for reg in registros_crudos
    ]

    print(f"\n[1] REGISTROS SANITIZADOS (Ubicación por defecto: '{ubicacion_default}'):")
    for s in sensores_limpios:
        print(f"  -> ID: {s['sensor_id']} | Temp: {s['temperatura']} ºC | Ubicación: {s['ubicación']}")

    # 4. Ejecutamos el análisis estadístico del Punto B utilizando el umbral estipulado
    alertas, promedio = generar_resumen_sensores(sensores_limpios, umbral_temperatura=umbral_limite)

    print(f"\n[2] REPORTE CONSOLIDADO PARA TOMA DE DECISIONES (Umbral: {umbral_limite} ºC):")
    print(f"   • Promedio térmico global de la planta: {promedio:.2f} ºC")
    print(f"   • Cantidad de dispositivos en estado de alerta: {len(alertas)}")
    print(f"   • IDs de sensores que superan el umbral: {alertas}")
    print("\n=== FIN DE LA EJECUCIÓN ===")
# ```[cite: 3]