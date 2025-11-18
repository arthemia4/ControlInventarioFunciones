# inventario_gui.py
# -----------------------------------------
# Interfaz Gráfica - Control de Inventario BioSalud Natural SpA
# -----------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import List, Dict
import csv
import os

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Inventario - BioSalud Natural SpA")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f0f0f0")
        
        # Datos del sistema
        self.catalogo: List[Dict] = []
        self.movimientos: List[List] = []
        self.stock_inicial: Dict[int, float] = {}
        
        # Cargar catálogo inicial por defecto
        self._cargar_catalogo_default()
        
        # Crear la interfaz
        self._crear_widgets()
        self._actualizar_tablas()
    
    def _cargar_catalogo_default(self):
        """Carga el catálogo por defecto"""
        self.catalogo = [
            {"id": 1, "nombre": "Faja magnética", "costo": 8990.0, "precio": 17990.0},
            {"id": 2, "nombre": "Rodillera térmica", "costo": 6990.0, "precio": 14990.0},
            {"id": 3, "nombre": "Pulsera energética", "costo": 1990.0, "precio": 4990.0},
        ]
        self.stock_inicial = {p["id"]: 0.0 for p in self.catalogo}
    
    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Marco superior - Título y botones principales
        frame_top = tk.Frame(self.root, bg="#2c3e50", height=80)
        frame_top.pack(fill=tk.X, padx=0, pady=0)
        
        titulo = tk.Label(frame_top, text="📦 CONTROL DE INVENTARIO", 
                         font=("Arial", 20, "bold"), bg="#2c3e50", fg="white")
        titulo.pack(pady=20)
        
        # Frame para botones de importar/exportar
        frame_botones = tk.Frame(self.root, bg="#f0f0f0")
        frame_botones.pack(fill=tk.X, padx=20, pady=10)
        
        btn_importar = tk.Button(frame_botones, text="📂 Importar CSV", 
                                command=self._importar_csv, 
                                bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                                padx=15, pady=8, cursor="hand2")
        btn_importar.pack(side=tk.LEFT, padx=5)
        
        btn_exportar = tk.Button(frame_botones, text="💾 Exportar CSV", 
                                command=self._exportar_csv,
                                bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                                padx=15, pady=8, cursor="hand2")
        btn_exportar.pack(side=tk.LEFT, padx=5)
        
        btn_actualizar = tk.Button(frame_botones, text="🔄 Actualizar", 
                                  command=self._actualizar_tablas,
                                  bg="#95a5a6", fg="white", font=("Arial", 10, "bold"),
                                  padx=15, pady=8, cursor="hand2")
        btn_actualizar.pack(side=tk.LEFT, padx=5)
        
        # Frame principal con pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Pestaña 1: Catálogo
        self.tab_catalogo = tk.Frame(notebook, bg="white")
        notebook.add(self.tab_catalogo, text="📋 Catálogo de Productos")
        self._crear_tab_catalogo()
        
        # Pestaña 2: Movimientos
        self.tab_movimientos = tk.Frame(notebook, bg="white")
        notebook.add(self.tab_movimientos, text="📊 Movimientos")
        self._crear_tab_movimientos()
        
        # Pestaña 3: Resumen
        self.tab_resumen = tk.Frame(notebook, bg="white")
        notebook.add(self.tab_resumen, text="💰 Resumen Financiero")
        self._crear_tab_resumen()
    
    def _crear_tab_catalogo(self):
        """Crea la pestaña de catálogo"""
        
        # Frame para la tabla
        frame_tabla = tk.Frame(self.tab_catalogo, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabla de productos
        columnas = ("ID", "Nombre", "Costo", "Precio", "Stock")
        self.tree_catalogo = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Configurar columnas
        self.tree_catalogo.heading("ID", text="ID")
        self.tree_catalogo.heading("Nombre", text="Nombre Producto")
        self.tree_catalogo.heading("Costo", text="Costo ($)")
        self.tree_catalogo.heading("Precio", text="Precio Venta ($)")
        self.tree_catalogo.heading("Stock", text="Stock Actual")
        
        self.tree_catalogo.column("ID", width=50, anchor=tk.CENTER)
        self.tree_catalogo.column("Nombre", width=250, anchor=tk.W)
        self.tree_catalogo.column("Costo", width=120, anchor=tk.E)
        self.tree_catalogo.column("Precio", width=120, anchor=tk.E)
        self.tree_catalogo.column("Stock", width=100, anchor=tk.E)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree_catalogo.yview)
        self.tree_catalogo.configure(yscrollcommand=scrollbar.set)
        
        self.tree_catalogo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botones de gestión
        frame_gestion = tk.Frame(self.tab_catalogo, bg="white")
        frame_gestion.pack(fill=tk.X, padx=10, pady=10)
        
        btn_agregar = tk.Button(frame_gestion, text="➕ Agregar Producto", 
                               command=self._agregar_producto,
                               bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                               padx=12, pady=6, cursor="hand2")
        btn_agregar.pack(side=tk.LEFT, padx=5)
        
        btn_editar = tk.Button(frame_gestion, text="✏️ Editar Producto", 
                              command=self._editar_producto,
                              bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                              padx=12, pady=6, cursor="hand2")
        btn_editar.pack(side=tk.LEFT, padx=5)
        
        btn_eliminar = tk.Button(frame_gestion, text="🗑️ Eliminar Producto", 
                                command=self._eliminar_producto,
                                bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                                padx=12, pady=6, cursor="hand2")
        btn_eliminar.pack(side=tk.LEFT, padx=5)
    
    def _crear_tab_movimientos(self):
        """Crea la pestaña de movimientos"""
        
        # Frame superior para registrar movimientos
        frame_registro = tk.LabelFrame(self.tab_movimientos, text="Registrar Movimiento", 
                                      font=("Arial", 11, "bold"), bg="white", padx=15, pady=15)
        frame_registro.pack(fill=tk.X, padx=10, pady=10)
        
        # Fila 1: Producto
        tk.Label(frame_registro, text="Producto:", bg="white", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_producto = ttk.Combobox(frame_registro, width=30, state="readonly")
        self.combo_producto.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Fila 2: Tipo de movimiento
        tk.Label(frame_registro, text="Tipo:", bg="white", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.var_tipo = tk.StringVar(value="Entrada")
        frame_tipo = tk.Frame(frame_registro, bg="white")
        frame_tipo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Radiobutton(frame_tipo, text="Entrada", variable=self.var_tipo, value="Entrada", 
                      bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame_tipo, text="Salida", variable=self.var_tipo, value="Salida", 
                      bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        # Fila 3: Cantidad
        tk.Label(frame_registro, text="Cantidad:", bg="white", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_cantidad = tk.Entry(frame_registro, width=15, font=("Arial", 10))
        self.entry_cantidad.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botón registrar
        btn_registrar = tk.Button(frame_registro, text="✅ Registrar Movimiento", 
                                 command=self._registrar_movimiento,
                                 bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                                 padx=15, pady=8, cursor="hand2")
        btn_registrar.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Tabla de movimientos
        frame_tabla = tk.Frame(self.tab_movimientos, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columnas = ("Fecha", "Producto", "Entrada", "Salida")
        self.tree_movimientos = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        
        self.tree_movimientos.heading("Fecha", text="Fecha")
        self.tree_movimientos.heading("Producto", text="Producto")
        self.tree_movimientos.heading("Entrada", text="Entrada (+)")
        self.tree_movimientos.heading("Salida", text="Salida (-)")
        
        self.tree_movimientos.column("Fecha", width=120, anchor=tk.CENTER)
        self.tree_movimientos.column("Producto", width=250, anchor=tk.W)
        self.tree_movimientos.column("Entrada", width=100, anchor=tk.E)
        self.tree_movimientos.column("Salida", width=100, anchor=tk.E)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree_movimientos.yview)
        self.tree_movimientos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_movimientos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _crear_tab_resumen(self):
        """Crea la pestaña de resumen financiero"""
        
        # Frame principal
        frame_principal = tk.Frame(self.tab_resumen, bg="white")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Título
        titulo = tk.Label(frame_principal, text="💰 RESUMEN FINANCIERO", 
                         font=("Arial", 16, "bold"), bg="white", fg="#2c3e50")
        titulo.pack(pady=20)
        
        # Frame para las tarjetas
        frame_tarjetas = tk.Frame(frame_principal, bg="white")
        frame_tarjetas.pack(pady=20)
        
        # Tarjeta 1: Valor Inventario
        self._crear_tarjeta(frame_tarjetas, "VALOR DEL INVENTARIO", 
                           "Σ (stock × costo)", "#3498db", 0)
        
        # Tarjeta 2: Valor Venta Potencial
        self._crear_tarjeta(frame_tarjetas, "VALOR VENTA POTENCIAL", 
                           "Σ (stock × precio)", "#27ae60", 1)
        
        # Tarjeta 3: Utilidad Potencial
        self._crear_tarjeta(frame_tarjetas, "UTILIDAD POTENCIAL", 
                           "Venta - Costo", "#f39c12", 2)
        
        # Frame para gráfico de productos
        frame_productos = tk.LabelFrame(frame_principal, text="Stock por Producto", 
                                       font=("Arial", 12, "bold"), bg="white", padx=15, pady=15)
        frame_productos.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.text_stock = tk.Text(frame_productos, height=10, font=("Courier", 10), 
                                 bg="#f8f9fa", relief=tk.FLAT, padx=10, pady=10)
        self.text_stock.pack(fill=tk.BOTH, expand=True)
    
    def _crear_tarjeta(self, parent, titulo, subtitulo, color, columna):
        """Crea una tarjeta de información"""
        frame = tk.Frame(parent, bg=color, relief=tk.RAISED, borderwidth=2)
        frame.grid(row=0, column=columna, padx=15, pady=10, sticky="nsew")
        
        tk.Label(frame, text=titulo, font=("Arial", 11, "bold"), 
                bg=color, fg="white").pack(pady=(15, 5))
        
        label_valor = tk.Label(frame, text="$0.00", font=("Arial", 20, "bold"), 
                              bg=color, fg="white")
        label_valor.pack(pady=5)
        
        tk.Label(frame, text=subtitulo, font=("Arial", 9), 
                bg=color, fg="white").pack(pady=(5, 15))
        
        # Guardar referencia para actualizar
        if columna == 0:
            self.label_valor_inv = label_valor
        elif columna == 1:
            self.label_valor_venta = label_valor
        else:
            self.label_utilidad = label_valor
    
    def _actualizar_combo_productos(self):
        """Actualiza el combo de productos"""
        productos = [f"{p['id']} - {p['nombre']}" for p in self.catalogo]
        self.combo_producto['values'] = productos
        if productos:
            self.combo_producto.current(0)
    
    def _actualizar_tablas(self):
        """Actualiza todas las tablas y resúmenes"""
        self._actualizar_tabla_catalogo()
        self._actualizar_tabla_movimientos()
        self._actualizar_resumen()
        self._actualizar_combo_productos()
    
    def _actualizar_tabla_catalogo(self):
        """Actualiza la tabla del catálogo"""
        # Limpiar tabla
        for item in self.tree_catalogo.get_children():
            self.tree_catalogo.delete(item)
        
        # Obtener stock actual
        stock = self._vector_stock_actual()
        
        # Llenar tabla
        for p in self.catalogo:
            s = stock.get(p['id'], 0.0)
            self.tree_catalogo.insert("", tk.END, values=(
                p['id'],
                p['nombre'],
                f"${p['costo']:,.2f}",
                f"${p['precio']:,.2f}",
                f"{s:.2f}"
            ))
    
    def _actualizar_tabla_movimientos(self):
        """Actualiza la tabla de movimientos"""
        # Limpiar tabla
        for item in self.tree_movimientos.get_children():
            self.tree_movimientos.delete(item)
        
        # Llenar tabla (mostrar más recientes primero)
        for mov in reversed(self.movimientos):
            fecha, pid, ent, sal = mov
            # Buscar nombre del producto
            nombre = next((p['nombre'] for p in self.catalogo if p['id'] == pid), f"ID {pid}")
            
            self.tree_movimientos.insert("", tk.END, values=(
                fecha,
                nombre,
                f"{ent:.2f}" if ent > 0 else "-",
                f"{sal:.2f}" if sal > 0 else "-"
            ))
    
    def _actualizar_resumen(self):
        """Actualiza el resumen financiero"""
        valor_inv = self._valor_inventario()
        valor_venta = self._valor_venta_potencial()
        utilidad = valor_venta - valor_inv
        
        self.label_valor_inv.config(text=f"${valor_inv:,.2f}")
        self.label_valor_venta.config(text=f"${valor_venta:,.2f}")
        self.label_utilidad.config(text=f"${utilidad:,.2f}")
        
        # Actualizar texto de stock
        self.text_stock.delete(1.0, tk.END)
        stock = self._vector_stock_actual()
        
        self.text_stock.insert(tk.END, f"{'Producto':<30} {'Stock':>10} {'Valor Inv.':>15} {'Valor Venta':>15}\n")
        self.text_stock.insert(tk.END, "="*75 + "\n")
        
        for p in self.catalogo:
            s = stock.get(p['id'], 0.0)
            v_inv = s * p['costo']
            v_venta = s * p['precio']
            self.text_stock.insert(tk.END, 
                f"{p['nombre']:<30} {s:>10.2f} ${v_inv:>13,.2f} ${v_venta:>13,.2f}\n")
    
    # ========== FUNCIONES DE NEGOCIO ==========
    
    def _vector_stock_actual(self) -> Dict[int, float]:
        """Calcula el stock actual por producto"""
        stock = {pid: round(self.stock_inicial.get(pid, 0.0), 2) for pid in self.stock_inicial}
        for fecha, pid, ent, sal in self.movimientos:
            stock[pid] = round(stock.get(pid, 0.0) + ent - sal, 2)
        return stock
    
    def _valor_inventario(self) -> float:
        """Calcula el valor total del inventario"""
        stock = self._vector_stock_actual()
        total = sum(stock.get(p['id'], 0.0) * p['costo'] for p in self.catalogo)
        return round(total, 2)
    
    def _valor_venta_potencial(self) -> float:
        """Calcula el valor de venta potencial"""
        stock = self._vector_stock_actual()
        total = sum(stock.get(p['id'], 0.0) * p['precio'] for p in self.catalogo)
        return round(total, 2)
    
    # ========== ACCIONES ==========
    
    def _agregar_producto(self):
        """Abre ventana para agregar un nuevo producto"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Producto")
        ventana.geometry("400x300")
        ventana.configure(bg="white")
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Calcular nuevo ID
        nuevo_id = max([p['id'] for p in self.catalogo], default=0) + 1
        
        # Campos
        tk.Label(ventana, text=f"ID: {nuevo_id}", bg="white", font=("Arial", 10)).pack(pady=10)
        
        tk.Label(ventana, text="Nombre del Producto:", bg="white", font=("Arial", 10)).pack(pady=5)
        entry_nombre = tk.Entry(ventana, width=30, font=("Arial", 10))
        entry_nombre.pack(pady=5)
        
        tk.Label(ventana, text="Costo ($):", bg="white", font=("Arial", 10)).pack(pady=5)
        entry_costo = tk.Entry(ventana, width=30, font=("Arial", 10))
        entry_costo.pack(pady=5)
        
        tk.Label(ventana, text="Precio de Venta ($):", bg="white", font=("Arial", 10)).pack(pady=5)
        entry_precio = tk.Entry(ventana, width=30, font=("Arial", 10))
        entry_precio.pack(pady=5)
        
        def guardar():
            try:
                nombre = entry_nombre.get().strip()
                costo = float(entry_costo.get().replace(',', '.'))
                precio = float(entry_precio.get().replace(',', '.'))
                
                if not nombre:
                    messagebox.showerror("Error", "El nombre es obligatorio")
                    return
                
                if costo <= 0 or precio <= 0:
                    messagebox.showerror("Error", "Costo y precio deben ser mayores a 0")
                    return
                
                self.catalogo.append({
                    "id": nuevo_id,
                    "nombre": nombre,
                    "costo": round(costo, 2),
                    "precio": round(precio, 2)
                })
                self.stock_inicial[nuevo_id] = 0.0
                
                self._actualizar_tablas()
                messagebox.showinfo("Éxito", "Producto agregado correctamente")
                ventana.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Verifique que costo y precio sean números válidos")
        
        tk.Button(ventana, text="Guardar", command=guardar, 
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(pady=20)
    
    def _editar_producto(self):
        """Edita el producto seleccionado"""
        seleccion = self.tree_catalogo.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
            return
        
        item = self.tree_catalogo.item(seleccion[0])
        pid = int(item['values'][0])
        producto = next((p for p in self.catalogo if p['id'] == pid), None)
        
        if not producto:
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Producto")
        ventana.geometry("400x300")
        ventana.configure(bg="white")
        ventana.transient(self.root)
        ventana.grab_set()
        
        tk.Label(ventana, text=f"ID: {pid}", bg="white", font=("Arial", 10)).pack(pady=10)
        
        tk.Label(ventana, text="Nombre del Producto:", bg="white", font=("Arial", 10)).pack(pady=5)
        entry_nombre = tk.Entry(ventana, width=30, font=("Arial", 10))
        entry_nombre.insert(0, producto['nombre'])
        entry_nombre.pack(pady=5)
        
        tk.Label(ventana, text="Costo ($):", bg="white", font=("Arial", 10)).pack(pady=5)
        entry_costo = tk.Entry(ventana, width=30, font=("Arial", 10))
        entry_costo.insert(0, producto['costo'])
        entry_costo.pack(pady=5)
        
        tk.Label(ventana, text="Precio de Venta ($):", bg="white", font=("Arial", 10)).pack(pady=5)
        entry_precio = tk.Entry(ventana, width=30, font=("Arial", 10))
        entry_precio.insert(0, producto['precio'])
        entry_precio.pack(pady=5)
        
        def guardar():
            try:
                nombre = entry_nombre.get().strip()
                costo = float(entry_costo.get().replace(',', '.'))
                precio = float(entry_precio.get().replace(',', '.'))
                
                if not nombre:
                    messagebox.showerror("Error", "El nombre es obligatorio")
                    return
                
                producto['nombre'] = nombre
                producto['costo'] = round(costo, 2)
                producto['precio'] = round(precio, 2)
                
                self._actualizar_tablas()
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                ventana.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Verifique que costo y precio sean números válidos")
        
        tk.Button(ventana, text="Guardar Cambios", command=guardar, 
                 bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(pady=20)
    
    def _eliminar_producto(self):
        """Elimina el producto seleccionado"""
        seleccion = self.tree_catalogo.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
        
        item = self.tree_catalogo.item(seleccion[0])
        pid = int(item['values'][0])
        nombre = item['values'][1]
        
        # Verificar si tiene movimientos
        tiene_movimientos = any(mov[1] == pid for mov in self.movimientos)
        
        if tiene_movimientos:
            msg = f"El producto '{nombre}' tiene movimientos registrados.\n¿Está seguro de eliminarlo? Los movimientos también se eliminarán."
        else:
            msg = f"¿Está seguro de eliminar el producto '{nombre}'?"
        
        if messagebox.askyesno("Confirmar", msg):
            # Eliminar producto
            self.catalogo = [p for p in self.catalogo if p['id'] != pid]
            # Eliminar movimientos
            self.movimientos = [m for m in self.movimientos if m[1] != pid]
            # Eliminar stock inicial
            if pid in self.stock_inicial:
                del self.stock_inicial[pid]
            
            self._actualizar_tablas()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
    
    def _registrar_movimiento(self):
        """Registra un nuevo movimiento"""
        try:
            if not self.combo_producto.get():
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return
            
            # Extraer ID del producto
            pid = int(self.combo_producto.get().split(' - ')[0])
            cantidad = float(self.entry_cantidad.get().replace(',', '.'))
            
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
            
            fecha = datetime.now().strftime("%Y-%m-%d")
            
            if self.var_tipo.get() == "Entrada":
                self.movimientos.append([fecha, pid, round(cantidad, 2), 0.0])
            else:
                # Verificar stock suficiente
                stock_actual = self._vector_stock_actual().get(pid, 0.0)
                if cantidad > stock_actual:
                    messagebox.showerror("Error", 
                        f"Stock insuficiente. Disponible: {stock_actual:.2f}")
                    return
                self.movimientos.append([fecha, pid, 0.0, round(cantidad, 2)])
            
            self.entry_cantidad.delete(0, tk.END)
            self._actualizar_tablas()
            messagebox.showinfo("Éxito", "Movimiento registrado correctamente")
            
        except ValueError:
            messagebox.showerror("Error", "Verifique que la cantidad sea un número válido")
    
    def _importar_csv(self):
        """Importa datos desde un archivo CSV"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta:
            return
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
            
            # Parsear el CSV
            nuevo_catalogo = []
            nuevos_movimientos = []
            
            seccion = None
            for linea in lineas:
                linea = linea.strip()
                if not linea or linea.startswith('=='):
                    continue
                
                if linea == 'CATALOGO':
                    seccion = 'CATALOGO'
                    continue
                elif linea == 'MOVIMIENTOS':
                    seccion = 'MOVIMIENTOS'
                    continue
                elif linea == 'RESUMEN':
                    seccion = None
                    continue
                
                if seccion == 'CATALOGO':
                    if linea.startswith('id,'):
                        continue
                    partes = linea.split(',')
                    if len(partes) >= 4:
                        try:
                            nuevo_catalogo.append({
                                'id': int(partes[0]),
                                'nombre': partes[1],
                                'costo': float(partes[2]),
                                'precio': float(partes[3])
                            })
                        except ValueError:
                            pass
                
                elif seccion == 'MOVIMIENTOS':
                    if linea.startswith('fecha,'):
                        continue
                    partes = linea.split(',')
                    if len(partes) >= 4:
                        try:
                            nuevos_movimientos.append([
                                partes[0],
                                int(partes[1]),
                                float(partes[2]),
                                float(partes[3])
                            ])
                        except ValueError:
                            pass
            
            # Actualizar datos
            if nuevo_catalogo:
                self.catalogo = nuevo_catalogo
                self.stock_inicial = {p['id']: 0.0 for p in self.catalogo}
            
            if nuevos_movimientos:
                self.movimientos = nuevos_movimientos
            
            self._actualizar_tablas()
            messagebox.showinfo("Éxito", f"Datos importados correctamente desde:\n{ruta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar CSV:\n{str(e)}")
    
    def _exportar_csv(self):
        """Exporta datos a un archivo CSV"""
        ruta = filedialog.asksaveasfilename(
            title="Guardar archivo CSV",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta:
            return
        
        try:
            stock = self._vector_stock_actual()
            
            with open(ruta, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(["== REPORTE INVENTARIO BIO SALUD NATURAL SpA =="])
                w.writerow([])
                w.writerow(["CATALOGO"])
                w.writerow(["id", "nombre", "costo", "precio", "stock_actual"])
                for p in self.catalogo:
                    w.writerow([p['id'], p['nombre'], f"{p['costo']:.2f}", 
                               f"{p['precio']:.2f}", f"{stock.get(p['id'], 0.0):.2f}"])
                
                w.writerow([])
                w.writerow(["RESUMEN"])
                w.writerow(["valor_inventario", f"{self._valor_inventario():.2f}"])
                w.writerow(["valor_venta_potencial", f"{self._valor_venta_potencial():.2f}"])
                
                w.writerow([])
                w.writerow(["MOVIMIENTOS"])
                w.writerow(["fecha", "id_producto", "entrada", "salida"])
                for mov in self.movimientos:
                    fecha, pid, ent, sal = mov
                    w.writerow([fecha, pid, f"{ent:.2f}", f"{sal:.2f}"])
            
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{ruta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar CSV:\n{str(e)}")


def main():
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
