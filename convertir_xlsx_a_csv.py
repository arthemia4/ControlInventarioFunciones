# convertir_xlsx_a_csv.py
# Convierte el archivo Excel a formato CSV compatible con el inventario

import openpyxl
import csv
from datetime import datetime

def convertir_excel_a_csv(archivo_excel, archivo_csv):
    """Convierte un archivo Excel a CSV formato inventario"""
    
    # Leer el archivo Excel
    wb = openpyxl.load_workbook(archivo_excel, data_only=True)
    ws = wb.active
    
    # Preparar datos para el CSV
    productos = {}
    contador_id = 1
    
    # Leer todas las filas (saltando encabezados)
    for i, fila in enumerate(ws.iter_rows(values_only=True), start=1):
        if i <= 4:  # Saltar encabezados
            continue
            
        if not any(fila):  # Saltar filas vacías
            continue
        
        # Extraer datos relevantes
        # Columnas: IMAGEN, FECHA COMPRA, NOMBRE PRODUCTO, CANT COMPRADA, VALOR UNITARIO COMPRA, 
        # VALOR TOTAL COMPRA, PROVEEDOR, fecha llegada, FECHA VENTA, PRECIO UNITARIO VENTA, 
        # CANT VENDIDA, VENTA TOTAL, A QUIEN VENDI, SALDO STOCK, STOCK CON VALORES
        
        try:
            fecha_compra = fila[2] if fila[2] else None
            nombre_producto = str(fila[3]).strip() if fila[3] else None
            cant_comprada = fila[4] if fila[4] else 0
            valor_unitario = fila[5] if fila[5] else 0
            precio_venta = fila[10] if len(fila) > 10 and fila[10] else 0
            cant_vendida = fila[11] if len(fila) > 11 and fila[11] else 0
            saldo_stock = fila[14] if len(fila) > 14 and fila[14] else 0
            
            # Validar que sea un producto válido
            if not nombre_producto or nombre_producto.startswith('='):
                continue
                
            # Convertir valores a números
            if isinstance(cant_comprada, str) and cant_comprada.startswith('='):
                continue
            if isinstance(valor_unitario, str) and valor_unitario.startswith('='):
                continue
            if isinstance(precio_venta, str) and precio_venta.startswith('='):
                precio_venta = 0
            if isinstance(cant_vendida, str) and cant_vendida.startswith('='):
                cant_vendida = 0
            if isinstance(saldo_stock, str) and saldo_stock.startswith('='):
                saldo_stock = 0
                
            cant_comprada = float(cant_comprada) if cant_comprada else 0
            valor_unitario = float(valor_unitario) if valor_unitario else 0
            precio_venta = float(precio_venta) if precio_venta else valor_unitario * 2
            cant_vendida = float(cant_vendida) if cant_vendida else 0
            saldo_stock = float(saldo_stock) if saldo_stock else 0
            
            if valor_unitario == 0 or cant_comprada == 0:
                continue
            
            # Agrupar productos similares
            if nombre_producto not in productos:
                productos[nombre_producto] = {
                    'id': contador_id,
                    'nombre': nombre_producto,
                    'costo': valor_unitario,
                    'precio': precio_venta if precio_venta > 0 else valor_unitario * 2,
                    'stock_total': 0,
                    'compras': []
                }
                contador_id += 1
            
            # Actualizar con el último precio si es mayor
            if precio_venta > productos[nombre_producto]['precio']:
                productos[nombre_producto]['precio'] = precio_venta
            
            # Calcular stock (comprado - vendido)
            stock_linea = cant_comprada - cant_vendida
            productos[nombre_producto]['stock_total'] += stock_linea
            
            # Guardar info de compra
            if isinstance(fecha_compra, datetime):
                fecha_str = fecha_compra.strftime("%Y-%m-%d")
            else:
                fecha_str = datetime.now().strftime("%Y-%m-%d")
                
            productos[nombre_producto]['compras'].append({
                'fecha': fecha_str,
                'cantidad': cant_comprada
            })
            
        except (ValueError, TypeError, IndexError) as e:
            continue
    
    print(f"\nProductos únicos encontrados: {len(productos)}")
    
    # Convertir diccionario a lista
    catalogo = list(productos.values())
    
    # Crear archivo CSV en formato compatible
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        
        w.writerow(["== REPORTE INVENTARIO BIO SALUD NATURAL SpA =="])
        w.writerow([])
        w.writerow(["CATALOGO"])
        w.writerow(["id", "nombre", "costo", "precio", "stock_actual"])
        
        for p in catalogo:
            w.writerow([
                p['id'],
                p['nombre'],
                f"{p['costo']:.2f}",
                f"{p['precio']:.2f}",
                f"{p['stock_total']:.2f}"
            ])
        
        w.writerow([])
        w.writerow(["RESUMEN"])
        valor_inv = sum(p['stock_total'] * p['costo'] for p in catalogo)
        valor_venta = sum(p['stock_total'] * p['precio'] for p in catalogo)
        w.writerow(["valor_inventario", f"{valor_inv:.2f}"])
        w.writerow(["valor_venta_potencial", f"{valor_venta:.2f}"])
        
        w.writerow([])
        w.writerow(["MOVIMIENTOS"])
        w.writerow(["fecha", "id_producto", "entrada", "salida"])
        
        # Crear movimientos de entrada basados en las compras
        for p in catalogo:
            for compra in p['compras']:
                w.writerow([compra['fecha'], p['id'], f"{compra['cantidad']:.2f}", "0.00"])
    
    print(f"\nArchivo CSV creado: {archivo_csv}")
    return True


if __name__ == "__main__":
    try:
        convertir_excel_a_csv(
            "Inventario BioSaludNaturalSpA.xlsx",
            "Inventario_BioSalud.csv"
        )
        print("\n✅ Conversión exitosa!")
        print("Archivo: Inventario_BioSalud.csv")
        
    except ImportError:
        print("Error: Se requiere instalar openpyxl")
        print("Ejecute: pip install openpyxl")
    except Exception as e:
        print(f"Error: {e}")
