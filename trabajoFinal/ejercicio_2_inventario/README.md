# Ejercicio 2: Modelo de Productos, Excepciones y Persistencia

Este módulo forma parte del proyecto final de **EcoTech Solutions** para el curso FESaT. Su objetivo principal es gestionar el catálogo de productos de la división de equipamiento sustentable, evitar inconsistencias en el inventario mediante validaciones de negocio y garantizar la persistencia del stock en archivos JSON.

---

## 📋 Descripción de la Consigna

El módulo implementa tres pilares fundamentales de la programación profesional en Python:

1. **Punto A (Dominio del Catálogo y Reglas de Inventario):**
   * **Excepción Personalizada:** Se define `StockInvalidoError` (heredando de `Exception`) para capturar e interrumpir de forma controlada la asignación de valores de stock negativos.
   * **Clase Base (`DispositivoEcológico`):** Implementa atributos protegidos y privados (`__precio_ars` encapsulado en pesos argentinos), métodos *getter* y *setter* para la modificación segura de atributos, y el método polimórfico `describir()`.
   * **Clase Derivada (`PanelSolar`):** Hereda de `DispositivoEcológico`, extiende la clase incorporando el atributo de potencia en watts (`potencia_w`), utiliza `super().__init__()` y sobrescribe el método `describir()` aplicando polimorfismo.

2. **Punto B (Persistencia y Gestor de Inventario):**
   * **Clase `GestorInventario`:** Contiene el método estático `guardar_catalogo_json(lista_dispositivos, ruta_archivo)` encargado de serializar las instancias a formato diccionario y guardarlas de forma estructurada e indentada en `catalogo_ecotech.json`.
   * **Bloque de Prueba:** Demuestra la captura exitosa de la excepción `StockInvalidoError` ante un stock erróneo y finaliza exportando los productos válidos a disco.

---

## 💻 Código Fuente (`main.py`)

```python
# =====================================================================
# EJERCICIO 2: MODELO DE PRODUCTOS, EXCEPCIONES Y PERSISTENCIA
# EcoTech Solutions - División de Equipamiento Sustentable
# =====================================================================

import json

# --- 1. EXCEPCIÓN PERSONALIZADA DE NEGOCIO ---
class StockInvalidoError(Exception):
    """
    Excepción personalizada que se eleva cuando se intenta asignar 
    un valor de stock negativo a un dispositivo o producto del inventario.
    """
    def __init__(self, stock_intentado: int, mensaje: str = "El stock no puede ser un valor negativo."):
        self.stock_intentado = stock_intentado
        self.mensaje = f"{mensaje} (Valor recibido: {stock_intentado})"
        super().__init__(self.mensaje)


# --- 2. CLASE BASE CON ENCAPSULAMIENTO ---
class DispositivoEcológico:
    """
    Clase base genérica que representa cualquier equipo sustentable 
    del catálogo de EcoTech Solutions.
    """
    def __init__(self, modelo: str, precio_ars: float, stock: int):
        self.modelo = modelo
        self.__precio_ars = float(precio_ars)   # Encapsulamiento explícito ($Arg)
        self.stock = 0
        self.set_stock(stock)                   # Validación segura mediante setter

    def get_precio_ars(self) -> float:
        """Getter seguro para acceder al precio privado."""
        return self.__precio_ars

    def set_stock(self, nuevo_stock: int):
        """Setter que aplica la regla de negocio impidiendo stock negativo."""
        if nuevo_stock < 0:
            raise StockInvalidoError(nuevo_stock)
        self.stock = nuevo_stock

    def describir(self) -> str:
        """Método sujeto a polimorfismo."""
        return f"Dispositivo Genérico - Modelo: {self.modelo}, Precio: ${self.__precio_ars:,.2f} ARS, Stock: {self.stock}"

    def a_diccionario(self) -> dict:
        """Serializa el objeto a diccionario para persitencia en JSON."""
        return {
            "tipo": "DispositivoEcológico",
            "modelo": self.modelo,
            "precio_ars": self.__precio_ars,
            "moneda": "ARS",
            "stock": self.stock
        }


# --- 3. CLASE DERIVADA (HERENCIA Y POLIMORFISMO) ---
class PanelSolar(DispositivoEcológico):
    """
    Clase especializada para paneles solares que hereda de DispositivoEcológico.
    """
    def __init__(self, modelo: str, precio_ars: float, stock: int, potencia_w: float):
        super().__init__(modelo, precio_ars, stock)
        self.potencia_w = float(potencia_w)

    def describir(self) -> str:
        """Sobrescritura del método describir (Polimorfismo)."""
        return f"Panel Solar [Modelo: {self.modelo} | Potencia: {self.potencia_w}W | Precio: ${self.get_precio_ars():,.2f} ARS | Stock: {self.stock} unidades]"

    def a_diccionario(self) -> dict:
        """Extiende el diccionario base con atributos específicos."""
        datos = super().a_diccionario()
        datos["tipo"] = "PanelSolar"
        datos["potencia_w"] = self.potencia_w
        return datos


# --- 4. GESTOR DE INVENTARIO Y PERSISTENCIA ---
class GestorInventario:
    """Clase responsable de la persistencia de productos en archivos JSON."""
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos: list, ruta_archivo: str):
        datos_serializables = [dispositivo.a_diccionario() for dispositivo in lista_dispositivos]
        
        with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
            json.dump(datos_serializables, archivo, indent=4, ensure_ascii=False)
        print(f"[ÉXITO] Catálogo exportado correctamente en '{ruta_archivo}'.")


# =====================================================================
# BLOQUE DE EJECUCIÓN Y PRUEBAS
# =====================================================================
if __name__ == "__main__":
    print("=== GESTIÓN DE INVENTARIO Y EQUIPAMIENTO SUSTENTABLE ===\n")
    
    catalogo_productos = []
    
    # 1. Captura controlada de StockInvalidoError
    try:
        print("Intentando registrar un producto con stock erróneo (-5)...")
        panel_erroneo = PanelSolar("EcoSun-100", 185000.0, -5, 300.0)
    except StockInvalidoError as error:
        print(f" -> [Excepción Capturada]: {error}\n")

    # 2. Registro de productos válidos y guardado en JSON
    try:
        panel_valido = PanelSolar("EcoSun-Max Pro", 374987.50, 15, 450.0)
        filtro_valido = DispositivoEcológico("Filtro Purificador H2O-Eco", 106875.00, 30)
        
        catalogo_productos.extend([panel_valido, filtro_valido])
        
        print("Fichas técnicas de productos registrados:")
        for prod in catalogo_productos:
            print("   •", prod.describir())
            
        print()
        GestorInventario.guardar_catalogo_json(catalogo_productos, "catalogo_ecotech.json")
        
    except Exception as ex:
        print(f"[ERROR INESPERADO]: {ex}")
```

---

## 📄 Archivo Generado (`catalogo_ecotech.json`)

```json
[
    {
        "tipo": "PanelSolar",
        "modelo": "EcoSun-Max Pro",
        "precio_ars": 374987.5,
        "moneda": "ARS",
        "stock": 15,
        "potencia_w": 450.0
    },
    {
        "tipo": "DispositivoEcológico",
        "modelo": "Filtro Purificador H2O-Eco",
        "precio_ars": 106875.0,
        "moneda": "ARS",
        "stock": 30
    }
]
```

---

## 🚀 Instrucciones de Ejecución

1. Asegúrate de contar con **Python 3.8+**.
2. Dirígete a la carpeta del ejercicio:
   ```bash
   cd ejercicio_2_inventario/
   ```
3. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```
4. Se generará automáticamente el archivo `catalogo_ecotech.json` en el mismo directorio.