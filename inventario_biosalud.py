# inventario_biosalud.py
# -----------------------------------------
# Control de Inventario - BioSalud Natural SpA
# Demuestra uso de: Funciones, Vectores y Matrices (listas de listas) + Sumatorias
# Formato de salida: 2 decimales
#
# Ejecución:
#   python inventario_biosalud.py
# -----------------------------------------

from datetime import datetime
from typing import List, Dict, Tuple
import csv
import os

# -----------------------------
# MODELO DE DATOS (SIMPLE)
# -----------------------------
# Catálogo base: vector de productos con costo y precio de referencia
CATALOGO: List[Dict] = [
    {"id": 1, "nombre": "Faja magnética", "costo": 8990.0, "precio": 17990.0},
    {"id": 2, "nombre": "Rodillera térmica", "costo": 6990.0, "precio": 14990.0},
    {"id": 3, "nombre": "Pulsera energética", "costo": 1990.0, "precio": 4990.0},
]

# Matriz de movimientos (filas): [fecha ISO, id_producto, entrada, salida]
MOVIMIENTOS: List[List] = []  # matriz vacía (se irá poblando)
# Ej: ["2025-11-17", 1, 10, 0]

# Vector de stock inicial por producto (alineado con CATALOGO por id)
STOCK_INICIAL: Dict[int, float] = {p["id"]: 0.0 for p in CATALOGO}

# -----------------------------
# FUNCIONES DE NEGOCIO (MATEMÁTICAS)
# -----------------------------

def _hoy_str() -> str:
    """Devuelve fecha en formato ISO (YYYY-MM-DD)."""
    return datetime.now().strftime("%Y-%m-%d")

def agregar_movimiento(id_producto: int, entrada: float, salida: float, fecha: str = None) -> None:
    """Agrega una fila a la matriz de movimientos. Usa 2 decimales en cantidades."""
    if fecha is None:
        fecha = _hoy_str()
    MOVIMIENTOS.append([fecha, id_producto, round(float(entrada), 2), round(float(salida), 2)])

def matriz_movimientos() -> List[List]:
    """Retorna la matriz completa de movimientos (copia)."""
    return [fila[:] for fila in MOVIMIENTOS]

def vector_stock_actual() -> Dict[int, float]:
    """
    Devuelve un vector (diccionario id->stock) con el stock actual por producto.
    Cálculo (sumatoria):
      stock_i = stock_inicial_i + Σ(entradas_i) - Σ(salidas_i)
    """
    stock = {pid: round(STOCK_INICIAL.get(pid, 0.0), 2) for pid in STOCK_INICIAL}
    for fecha, pid, ent, sal in MOVIMIENTOS:
        stock[pid] = round(stock.get(pid, 0.0) + ent - sal, 2)
    return stock

def stock_de_producto(id_producto: int) -> float:
    """Devuelve el stock actual de un producto específico (2 decimales)."""
    return round(vector_stock_actual().get(id_producto, 0.0), 2)

def valor_inventario() -> float:
    """
    Devuelve el valor total del inventario usando costo base del catálogo.
    Fórmula (sumatoria):
      Valor = Σ (stock_i * costo_i)
    """
    stock = vector_stock_actual()
    total = 0.0
    for p in CATALOGO:
        s_i = stock.get(p["id"], 0.0)
        total += s_i * p["costo"]
    return round(total, 2)

def valor_venta_potencial() -> float:
    """
    Valor de venta potencial si vendiéramos todo el stock al precio de referencia.
      Σ (stock_i * precio_i)
    """
    stock = vector_stock_actual()
    total = 0.0
    for p in CATALOGO:
        s_i = stock.get(p["id"], 0.0)
        total += s_i * p["precio"]
    return round(total, 2)

def funcion_stock_t(id_producto: int, movimientos_ordenados: List[List]) -> List[Tuple[str, float]]:
    """
    Función discreta f(t) = stock acumulado del producto i hasta el tiempo t (por fecha).
    Retorna lista de pares (fecha, stock_acumulado). Útil para mostrar la "función" en la PPT.
    """
    s = round(STOCK_INICIAL.get(id_producto, 0.0), 2)
    serie = []
    for fecha, pid, ent, sal in movimientos_ordenados:
        if pid == id_producto:
            s = round(s + ent - sal, 2)
        serie.append((fecha, s))
    return serie

# -----------------------------
# EXPORTACIÓN DE REPORTE
# -----------------------------

def exportar_csv(ruta: str = "reporte_inventario.csv") -> str:
    """Exporta el catálogo, stock y movimientos a un CSV sencillo."""
    stock = vector_stock_actual()
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["== REPORTE INVENTARIO BIO SALUD NATURAL SpA =="])
        w.writerow([])
        w.writerow(["CATALOGO"])
        w.writerow(["id", "nombre", "costo", "precio", "stock_actual"])
        for p in CATALOGO:
            w.writerow([p["id"], p["nombre"], f"{p['costo']:.2f}", f"{p['precio']:.2f}", f"{stock.get(p['id'], 0.0):.2f}"])
        w.writerow([])
        w.writerow(["RESUMEN"])
        w.writerow(["valor_inventario", f"{valor_inventario():.2f}"])
        w.writerow(["valor_venta_potencial", f"{valor_venta_potencial():.2f}"])
        w.writerow([])
        w.writerow(["MOVIMIENTOS"])
        w.writerow(["fecha", "id_producto", "entrada", "salida"])
        for fila in MOVIMIENTOS:
            fecha, pid, ent, sal = fila
            w.writerow([fecha, pid, f"{ent:.2f}", f"{sal:.2f}"])
    return os.path.abspath(ruta)

# -----------------------------
# DEMO RÁPIDA (para la diapositiva 7)
# -----------------------------

def demo() -> None:
    """
    Simula una corrida rápida para mostrar en la presentación:
      - Matriz de movimientos
      - Vector stock actual
      - Sumatorias de valor
      - Función stock f(t) de un producto
    """
    # Limpiar por si se ejecuta varias veces
    MOVIMIENTOS.clear()

    # Cargar algunos movimientos de ejemplo
    agregar_movimiento(1, 10, 0)   # +10 fajas
    agregar_movimiento(2, 15, 0)   # +15 rodilleras
    agregar_movimiento(3, 20, 0)   # +20 pulseras
    agregar_movimiento(1, 0, 2)    # -2 fajas (venta)
    agregar_movimiento(2, 0, 5)    # -5 rodilleras (venta)
    agregar_movimiento(3, 5, 0)    # +5 pulseras (reposición)

    print("=== DEMO: Control de Inventario BioSalud Natural SpA ===")
    print("Catálogo:")
    for p in CATALOGO:
        print(f"  {p['id']:>2} - {p['nombre']:<20}  Costo: ${p['costo']:.2f}  Precio: ${p['precio']:.2f}")

    print("\nMatriz de movimientos (fecha, id, entrada, salida):")
    for fila in matriz_movimientos():
        print(" ", fila)

    stock = vector_stock_actual()
    print("\nVector de stock actual (id -> unidades):")
    for pid, s in stock.items():
        print(f"  {pid}: {s:.2f} unidades")

    print(f"\nValor del inventario (Σ stock_i * costo_i): ${valor_inventario():.2f}")
    print(f"Valor de venta potencial (Σ stock_i * precio_i): ${valor_venta_potencial():.2f}")

    # Mostrar función stock f(t) para un producto (id=1)
    movs_ordenados = sorted(MOVIMIENTOS, key=lambda r: r[0])
    serie = funcion_stock_t(1, movs_ordenados)
    print("\nFunción stock f(t) para 'Faja magnética' (pares fecha, stock):")
    for fecha, s in serie:
        print(f"  ({fecha}, {s:.2f})")

    # Exportar CSV
    ruta = exportar_csv("reporte_inventario.csv")
    print(f"\nReporte exportado a: {ruta}")

# -----------------------------
# MENÚ SIMPLE (opcional para usar en laboratorio/clase)
# -----------------------------

def _mostrar_menu():
    print("\n=== MENÚ INVENTARIO ===")
    print("1) Ver catálogo")
    print("2) Registrar ENTRADA")
    print("3) Registrar SALIDA")
    print("4) Ver stock por producto")
    print("5) Ver resumen: valor inventario y venta potencial")
    print("6) Exportar CSV")
    print("7) DEMO rápida (recomendado para PPT)")
    print("0) Salir")

def _input_float(msg: str) -> float:
    while True:
        try:
            return round(float(input(msg).strip().replace(',', '.')), 2)
        except ValueError:
            print("Ingrese un número válido (use . o ,).")

def _input_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Ingrese un entero válido.")

def main():
    while True:
        _mostrar_menu()
        op = input("Opción: ").strip()
        if op == "1":
            print("\nCatálogo:")
            for p in CATALOGO:
                print(f"  {p['id']:>2} - {p['nombre']:<20}  Costo: ${p['costo']:.2f}  Precio: ${p['precio']:.2f}")
        elif op == "2":
            pid = _input_int("ID producto: ")
            cant = _input_float("Cantidad a ingresar: ")
            agregar_movimiento(pid, cant, 0.0)
            print("Entrada registrada.")
        elif op == "3":
            pid = _input_int("ID producto: ")
            cant = _input_float("Cantidad a descontar: ")
            agregar_movimiento(pid, 0.0, cant)
            print("Salida registrada.")
        elif op == "4":
            pid = _input_int("ID producto: ")
            print(f"Stock actual del producto {pid}: {stock_de_producto(pid):.2f} unidades")
        elif op == "5":
            print(f"Valor inventario: ${valor_inventario():.2f}")
            print(f"Valor venta potencial: ${valor_venta_potencial():.2f}")
        elif op == "6":
            ruta = exportar_csv()
            print(f"CSV exportado en: {ruta}")
        elif op == "7":
            demo()
        elif op == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    # Si quieres que al ejecutar se vea una demo automática, descomenta:
    # demo()
    # Si quieres menú interactivo, deja así:
    main()
