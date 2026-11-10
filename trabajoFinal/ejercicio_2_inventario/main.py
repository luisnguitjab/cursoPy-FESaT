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
    Hereda de la clase base Exception de Python.
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
        self.modelo = modelo                    # Atributo público para el identificador
        self.__precio_ars = float(precio_ars)   # Atributo PRIVADO encapsulado (en pesos argentinos)
        self.stock = 0                          # Inicializador seguro por defecto
        self.set_stock(stock)                   # Validación inicial mediante método setter

    # Método Getter para acceder de manera controlada al precio privado
    def get_precio_ars(self) -> float:
        """Retorna de forma segura el valor del precio encapsulado en pesos argentinos ($Arg)."""
        return self.__precio_ars

    # Método Setter para validar y modificar el stock de forma segura
    def set_stock(self, nuevo_stock: int):
        """
        Actualiza el stock del dispositivo validando que no sea negativo.
        Lanza StockInvalidoError en caso de incumplir la regla de negocio.
        """
        if nuevo_stock < 0:
            raise StockInvalidoError(nuevo_stock)
        self.stock = nuevo_stock

    # Método genérico sujeto a polimorfismo
    def describir(self) -> str:
        """Devuelve una ficha técnica general del dispositivo ecológico."""
        return f"Dispositivo Genérico - Modelo: {self.modelo}, Precio: ${self.__precio_ars:,.2f} ARS, Stock: {self.stock}"

    # Método para serializar el objeto a formato diccionario (útil para JSON)
    def a_diccionario(self) -> dict:
        """Convierte los atributos de la instancia en un diccionario plano serializable."""
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
    Clase especializada que hereda de DispositivoEcológico para representar 
    paneles solares con especificaciones técnicas particulares.
    """
    def __init__(self, modelo: str, precio_ars: float, stock: int, potencia_w: float):
        # Inicializamos los atributos heredados de la clase base
        super().__init__(modelo, precio_ars, stock)
        self.potencia_w = float(potencia_w)  # Atributo específico del panel solar

    # Sobrescritura del método describir (Polimorfismo)
    def describir(self) -> str:
        """Personaliza la emisión de la ficha técnica comercial para los paneles solares."""
        return f"Panel Solar [Modelo: {self.modelo} | Potencia: {self.potencia_w}W | Precio: ${self.get_precio_ars():,.2f} ARS | Stock: {self.stock} unidades]"

    # Sobrescritura del método de serialización para incluir la potencia
    def a_diccionario(self) -> dict:
        """Extiende el diccionario base agregando la potencia en watts."""
        datos = super().a_diccionario()
        datos["tipo"] = "PanelSolar"
        datos["potencia_w"] = self.potencia_w
        return datos


# --- 4. GESTOR DE INVENTARIO Y PERSISTENCIA EN DISCO ---
class GestorInventario:
    """
    Clase responsable de administrar el catálogo de productos y 
    gestionar su almacenamiento persistente en archivos estructurados.
    """
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos: list, ruta_archivo: str):
        """
        Recibe una lista de instancias de dispositivos, las convierte a diccionarios
        y las almacena en disco con formato JSON legible (indentado y con codificación UTF-8).
        """
        # Mapeamos cada objeto del catálogo a su representación en diccionario
        datos_serializables = [dispositivo.a_diccionario() for dispositivo in lista_dispositivos]
        
        # Abrimos el archivo en modo escritura ('w') con codificación UTF-8
        with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
            json.dump(datos_serializables, archivo, indent=4, ensure_ascii=False)
            
        print(f"[ÉXITO] Catálogo exportado correctamente en el archivo '{ruta_archivo}'.")


# =====================================================================
# BLOQUE DE PRUEBA Y VALIDACIÓN (DEMOSTRACIÓN DE EJECUCIÓN)
# =====================================================================
if __name__ == "__main__":
    print("=== GESTIÓN DE INVENTARIO Y EQUIPAMIENTO SUSTENTABLE - ECOTECH ===\n")
    
    catalogo_productos = []
    
    # 1. Prueba de captura de excepción controlada ante stock negativo
    try:
        print("Intentando registrar un panel solar con stock inválido (-5)...")
        panel_erroneo = PanelSolar(modelo="EcoSun-100", precio_ars=185000.0, stock=-5, potencia_w=300.0)
    except StockInvalidoError as error_negocio:
        print(f" -> [Excepción de Negocio Capturada]: {error_negocio}\n")

    # 2. Creación de registros válidos para el catálogo comercial
    try:
        # Instanciando un Panel Solar (Clase derivada con polimorfismo)
        panel_principal = PanelSolar(
            modelo="EcoSun-Max Pro", 
            precio_ars=374987.50, 
            stock=15, 
            potencia_w=450.0
        )
        
        # Instanciando un Dispositivo Ecológico Genérico (Clase base)
        filtro_agua = DispositivoEcológico(
            modelo="Filtro Purificador H2O-Eco", 
            precio_ars=106875.00, 
            stock=30
        )
        
        # Agregamos los productos válidos a la lista del catálogo
        catalogo_productos.extend([panel_principal, filtro_agua])
        
        print("Fichas técnicas de los productos válidos registrados en memoria:")
        for item in catalogo_productos:
            # Demostración de polimorfismo mediante el método describir()
            print("   •", item.describir())
            
        print()
        
        # 3. Persistencia de datos en disco utilizando el GestorInventario
        archivo_destino = "catalogo_ecotech.json"
        GestorInventario.guardar_catalogo_json(catalogo_productos, archivo_destino)
        
    except Exception as ex:
        print(f"[ERROR INESPERADO]: {ex}")
        
    print("\n=== FIN DE LA EJECUCIÓN DEL MÓDULO ===")
#```[cite: 3, 4]

#---

### **Estructura del Archivo JSON Generado (`catalogo_ecotech.json`)**

#Una vez ejecutado el bloque de pruebas, se creará automáticamente en tu directorio el archivo con el siguiente contenido estructurado en pesos argentinos[cite: 3]:

#```json
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