# 📦 Sistema de Control de Inventario - BioSalud Natural SpA

Sistema de gestión de inventario con interfaz gráfica desarrollado en Python usando Tkinter.

## 🌟 Características

- **Interfaz gráfica moderna** con pestañas organizadas
- **Gestión de productos**: Agregar, editar y eliminar productos
- **Control de movimientos**: Registrar entradas y salidas de inventario
- **Resumen financiero**: Valor del inventario, valor de venta potencial y utilidad
- **Importar/Exportar CSV**: Compatible con formato CSV personalizado
- **Precios en pesos chilenos (CLP)** redondeados

## 📁 Archivos del Proyecto

- `inventario_gui.py` - Interfaz gráfica principal
- `inventario_biosalud.py` - Sistema original con menú de consola
- `convertir_xlsx_a_csv.py` - Conversor de Excel a CSV compatible
- `Inventario_BioSalud.csv` - Datos de inventario
- `reporte_inventario_demo.csv` - Datos de demostración

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd proyectofunciones
```

2. Instala las dependencias:
```bash
pip install openpyxl
```

## 💻 Uso

### Interfaz Gráfica

```bash
python inventario_gui.py
```

### Sistema de Consola

```bash
python inventario_biosalud.py
```

### Convertir Excel a CSV

```bash
python convertir_xlsx_a_csv.py
```

## 📊 Funcionalidades

### Catálogo de Productos
- Visualización de todos los productos con stock actual
- Agregar nuevos productos con costo y precio de venta
- Editar información de productos existentes
- Eliminar productos del catálogo

### Movimientos de Inventario
- Registrar entradas de stock
- Registrar salidas con validación de stock disponible
- Historial completo de movimientos con fechas

### Resumen Financiero
- Valor total del inventario (costo)
- Valor de venta potencial
- Cálculo de utilidad potencial
- Detalle por producto

### Importar/Exportar
- Importar datos desde archivos CSV
- Exportar inventario completo a CSV
- Formato compatible con Excel

## 🔧 Requisitos

- Python 3.6 o superior
- tkinter (incluido con Python)
- openpyxl (para conversión de Excel)

## 📝 Formato CSV

El sistema utiliza un formato CSV específico:

```csv
== REPORTE INVENTARIO BIO SALUD NATURAL SpA ==

CATALOGO
id,nombre,costo,precio,stock_actual
1,Producto ejemplo,1000,2000,10.00

RESUMEN
valor_inventario,10000.00
valor_venta_potencial,20000.00

MOVIMIENTOS
fecha,id_producto,entrada,salida
2025-11-17,1,10.00,0.00
```

## 👨‍💻 Autor

Desarrollado para BioSalud Natural SpA

## 📄 Licencia

Este proyecto es de uso interno para BioSalud Natural SpA.
