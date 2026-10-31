"""
EVOLUCIÓN DE herramientas.py

Bitácora de este archivo, en el orden en que creció: 3 -> 4 -> 4b -> 4c -> 4d.
El archivo final está en proyecto_final/herramientas.py
"""


# ============================================================================
# PASO 3 · Las funciones (las "manos" del agente)
# ============================================================================

# NUEVO ARCHIVO. Son funciones normales de Python.


"""PIEZA 2 · LAS HERRAMIENTAS: las "manos" del agente. Son funciones normales de Python."""
from db import conectar


def buscar_producto(texto):
    con = conectar()
    filas = con.execute("SELECT nombre, stock, minimo, costo FROM productos WHERE nombre LIKE ?",
                        (f"%{texto}%",)).fetchall()
    con.close()
    return [dict(f) for f in filas]


def agregar_producto(nombre, stock, minimo, costo):
    con = conectar()
    con.execute("INSERT INTO productos (nombre, stock, minimo, costo) VALUES (?,?,?,?)",
                (nombre, stock, minimo, costo))
    con.commit()
    con.close()
    return {"agregado": nombre}


def quitar_producto(nombre):
    con = conectar()
    con.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))
    con.commit()
    con.close()
    return {"quitado": nombre}


def actualizar_producto(nombre, stock=None, minimo=None, costo=None):
    con = conectar()
    for campo, valor in (("stock", stock), ("minimo", minimo), ("costo", costo)):
        if valor is not None:
            con.execute(f"UPDATE productos SET {campo} = ? WHERE nombre = ?", (valor, nombre))
    con.commit()
    fila = con.execute("SELECT nombre, stock, minimo, costo FROM productos WHERE nombre = ?", (nombre,)).fetchone()
    con.close()
    return dict(fila)


def listar_stock_bajo(limite=None):
    con = conectar()
    filas = con.execute("""
        SELECT nombre, stock, minimo, costo,
          COALESCE((SELECT SUM(cantidad) FROM ordenes o WHERE o.producto_id = p.id AND o.estado = 'pendiente'), 0) AS en_camino
        FROM productos p WHERE stock <= COALESCE(?, minimo)""", (limite,)).fetchall()
    con.close()
    return [dict(f) for f in filas]


def crear_orden_compra(nombre, cantidad):
    con = conectar()
    p = con.execute("SELECT id, costo FROM productos WHERE nombre = ?", (nombre,)).fetchone()
    total = cantidad * p["costo"]
    con.execute("INSERT INTO ordenes (producto_id, cantidad, total) VALUES (?,?,?)", (p["id"], cantidad, total))
    con.commit()
    con.close()
    return {"orden": nombre, "cantidad": cantidad, "total": total}


def listar_productos():
    con = conectar()
    filas = con.execute("SELECT nombre, stock, minimo, costo FROM productos").fetchall()
    con.close()
    return [dict(f) for f in filas]


# ============================================================================
# PASO 4 · Cómo las ve el modelo
# ============================================================================

# Pégalo AL FINAL de herramientas.py. TOOLS = lo único que el modelo "ve"; FUNCIONES conecta nombre -> función; ejecutar corre lo que el modelo pidió y regresa el error en vez de tronar.


# ---------- cómo se las presentamos al modelo ----------
def _tool(nombre, descripcion, propiedades=None, requeridos=None):
    return {"type": "function", "function": {
        "name": nombre, "description": descripcion,
        "parameters": {"type": "object", "properties": propiedades or {}, "required": requeridos or []}}}


NOMBRE = {"type": "string", "description": "Nombre EXACTO del producto, como lo devuelve buscar_producto"}

TOOLS = [
    _tool("listar_productos", "Muestra TODOS los productos con su stock, mínimo y costo."),
    _tool("buscar_producto",
          "Busca productos cuyo nombre contenga un texto (en singular, ej. 'playera'). "
          "Úsala para conocer el stock actual y el nombre exacto de un producto.",
          {"texto": {"type": "string"}}, ["texto"]),
    _tool("agregar_producto", "Da de alta un producto NUEVO.",
          {"nombre": {"type": "string"}, "stock": {"type": "integer"},
           "minimo": {"type": "integer"}, "costo": {"type": "number"}},
          ["nombre", "stock", "minimo", "costo"]),
    _tool("quitar_producto", "Elimina un producto.", {"nombre": NOMBRE}, ["nombre"]),
    _tool("actualizar_producto",
          "Cambia el stock, el mínimo o el costo de un producto. El stock es el valor NUEVO, no una resta: "
          "para registrar una venta, busca primero el stock actual y calcula el nuevo.",
          {"nombre": NOMBRE, "stock": {"type": "integer"}, "minimo": {"type": "integer"},
           "costo": {"type": "number"}}, ["nombre"]),
    _tool("listar_stock_bajo",
          "Lista los productos con stock menor o igual a 'limite'. Sin límite, usa el mínimo de cada producto. "
          "Incluye 'en_camino': unidades que ya fueron pedidas.",
          {"limite": {"type": "integer"}}),
    _tool("crear_orden_compra", "Crea una orden de compra para reponer un producto.",
          {"nombre": NOMBRE, "cantidad": {"type": "integer"}}, ["nombre", "cantidad"]),
]

FUNCIONES = {f.__name__: f for f in (listar_productos, buscar_producto, agregar_producto, quitar_producto,
                                     actualizar_producto, listar_stock_bajo, crear_orden_compra)}


def ejecutar(nombre, args):
    """El harness ejecuta lo que el modelo pidió. Si algo falla, regresa el error (no truena)."""
    try:
        return FUNCIONES[nombre](**args)
    except Exception as e:
        return {"error": f"{nombre} falló: {e}"}


# ============================================================================
# PASO 4b · Agregar listar_ordenes y completar_orden
# ============================================================================

# 1) Las dos funciones, antes del bloque "cómo se las presentamos al modelo".


def listar_ordenes(estado=None):
    con = conectar()
    sql = ("SELECT o.id, p.nombre, o.cantidad, o.total, o.estado FROM ordenes o "
           "JOIN productos p ON p.id = o.producto_id")
    filas = con.execute(sql + (" WHERE o.estado = ?" if estado else ""), (estado,) if estado else ()).fetchall()
    con.close()
    return [dict(f) for f in filas]


def completar_orden(id):
    """La orden llegó: se marca como completada y las unidades entran al stock."""
    con = conectar()
    o = con.execute("SELECT producto_id, cantidad FROM ordenes WHERE id = ? AND estado = 'pendiente'", (id,)).fetchone()
    if not o:
        con.close()
        return {"error": f"No hay una orden pendiente con id {id}."}
    con.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (o["cantidad"], o["producto_id"]))
    con.execute("UPDATE ordenes SET estado = 'completada' WHERE id = ?", (id,))
    con.commit()
    con.close()
    return {"orden": id, "estado": "completada", "unidades_recibidas": o["cantidad"]}


# 2) En TOOLS, al final de la lista:


# _tool("listar_ordenes", "Lista las órdenes de compra con su id, producto, cantidad, total y estado. "
#           "Opcional: filtra por estado ('pendiente' o 'completada').",
#           {"estado": {"type": "string", "enum": ["pendiente", "completada"]}}),
#     _tool("completar_orden", "Marca una orden pendiente como recibida: suma sus unidades al stock. "
#           "Necesita el id de la orden (míralo en listar_ordenes).",
#           {"id": {"type": "integer"}}, ["id"]),


# 3) En FUNCIONES, agrega: listar_ordenes, completar_orden


# ============================================================================
# PASO 4c · Quitar la barrera de gasto
# ============================================================================

# Se borró LIMITE_ORDEN y el "if total > LIMITE_ORDEN" de crear_orden_compra. Solo happy path (la función del paso 3 ya está así).


# ============================================================================
# PASO 4d · Agregar notificar_gerente
# ============================================================================

# 1) La función, antes del bloque "cómo se las presentamos al modelo".


def notificar_gerente(mensaje):
    """Aquí solo lo imprimimos; en la vida real sería un correo, WhatsApp o Slack."""
    print(f"📣 AVISO AL GERENTE: {mensaje}")
    return {"notificado": True, "mensaje": mensaje}


# 2) En TOOLS, al final de la lista:


# _tool("notificar_gerente", "Envía un aviso al gerente. Úsala cuando un producto se quede sin stock (0) "
#           "para que lo revise. Escribe el mensaje con el nombre exacto del producto.",
#           {"mensaje": {"type": "string"}}, ["mensaje"]),


# 3) En FUNCIONES, agrega: notificar_gerente. Quedan 10 herramientas.
