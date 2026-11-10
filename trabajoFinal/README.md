# Proyecto Final de programación con Python - EcoTech Solutions

Este es el repositorio oficial del **Proyecto Final FESaT** para la empresa **EcoTech Solutions**. Este repositorio contiene una solución modular estructurada en tres ejercicios independientes que abarcan desde el procesamiento de datos crudos de microcontroladores y la programación orientada a objetos (POO), hasta la auditoría automatizada y el despliegue de un panel administrativo web en **Django**.

---

## Estructura general del repositorio

El proyecto se encuentra organizado en tres carpetas principales:

```text
trabajoFinal/
├── ejercicio_1_sensores/      # Sanitización y procesamiento de datos térmicos
├── ejercicio_2_inventario/    # Modelo POO, validación de stock y persistencia JSON
├── ejercicio_3_django/        # Auditoría con unittest e integración Web en Django
├── .gitignore                 # Archivos e historiales ignorados por Git
└── README.md                  # Documentación principal del repositorio
```

---

## Resumen de los ejercicios

### 1. Ejercicio 1: Sanitización y análisis estadístico de sensores (`ejercicio_1_sensores/`)
* **Propósito:** Normalizar lecturas térmicas de microcontroladores de campo que contienen espacios indeseados, unidades de medida mezcladas (`ºC`, `°C`, `ºc`, `°c`, `C`, `c`, `º`, `˚`, `⁰`) y atributos faltantes.
* **Características:**
  * Limpieza explícita de caracteres y asignación de ubicaciones por defecto seguro.
  * Reporte estadístico global (promedio térmico y detección de sensores en alerta según un umbral dinámico).
* **Ejecución:**
```  
  cd ejercicio_1_sensores/
  python main.py
```  
---

### 2. Ejercicio 2: Modelo de inventario, excepciones y JSON (`ejercicio_2_inventario/`)
* **Propósito:** Gestionar el catálogo de productos sustentables con encapsulamiento estricto en Pesos Argentinos (ARS) y persistencia en disco.
* **Características:**
  * Implementación de la excepción personalizada `StockInvalidoError` para evitar inconsistencias por stock negativo.
  * Jerarquía de clases (`DispositivoEcológico` -> `PanelSolar`) aplicando encapsulamiento y polimorfismo.
  * Exportación serializada al archivo `catalogo_ecotech.json` mediante `GestorInventario`.
* **Ejecución:**
```  
  cd ejercicio_2_inventario/
  python main.py
```  
---

### 3. Ejercicio 3: Auditoría automatizada y proyecto Web (`ejercicio_3_django/`)
* **Propósito:** Certificar mediante pruebas unitarias (`unittest`) la precisión del algoritmo de huella de carbono industrial e integrarlo en la tubería de datos que alimenta la vista web administrativa de Django.
* **Características:**
  * Algoritmo auditado contra casos nominales y captura de excepciones `ValueError`.
  * Vista web que procesa métricas globales e identifica la planta industrial de mayor consumo.
  * Interfaz de usuario renderizada mediante la plantilla HTML `panel.html`.

---

## Guía para ejecutar el proyecto Django (Ejercicio 3)

Los comandos para levantar el entorno web localmente:

### 1. Clonar el repositorio y navegar a la carpeta del ejercicio
```
git clone <URL_DE_TU_REPOSITORIO_GITHUB>
cd ecotech_solutions_proyecto_final/ejercicio_3_django/
```

### 2. Instalar las dependencias
*(Se recomienda activar previamente un entorno virtual)*
```
pip install -r requirements.txt
```

### 3. Ejecutar las pruebas unitarias (auditoría)
Para certificar que el algoritmo de emisiones de carbono cumple con todos los estándares requeridos:
```
python manage.py test sustentabilidad
```

### 4. Aplicar las migraciones base de Django
```
python manage.py migrate
```

### 5. Iniciar el servidor web de desarrollo
```
python manage.py runserver
```

### 6. Acceder a la interfaz web
Desde el navegador ingresar a:
```
*`http://127.0.0.1:8000/sustentabilidad/`** *(o simplemente `http://127.0.0.1:8000/`)*
```
---

## Tecnologías utilizadas
* **Lenguaje:** Python 3.8+
* **Framework Web:** Django 4.2+
* **Testing:** suite `unittest` / Django Test Runner
* **Persistencia:** formato JSON y SQLite3
* **Control de versiones:** Git & GitHub
