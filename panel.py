"""
EVOLUCIÓN DE panel.py

Bitácora de este archivo: se crea una vez (paso 9) y ya no cambia.
Requiere: py -m pip install rich
"""


# ============================================================================
# PASO 9 · Crear panel.py (tabla del inventario)
# ============================================================================

# NUEVO ARCHIVO. Prueba: from panel import mostrar_inventario; mostrar_inventario("Gorra azul")


"""PANEL: una tabla en la terminal para ver el inventario en vivo."""
from rich.console import Console
from rich.table import Table
from db import conectar

consola = Console()


def mostrar_inventario(resaltar=None):
    con = conectar()
    filas = con.execute("""
        SELECT nombre, stock, minimo,
          COALESCE((SELECT SUM(cantidad) FROM ordenes o WHERE o.producto_id = p.id AND o.estado = 'pendiente'), 0) AS en_camino
        FROM productos p""").fetchall()
    con.close()

    tabla = Table(title="📦 Inventario")
    tabla.add_column("Producto")
    tabla.add_column("Stock", justify="right")
    tabla.add_column("Mínimo", justify="right")
    tabla.add_column("En camino", justify="right")
    for f in filas:
        color = "red" if f["stock"] <= f["minimo"] else "green"
        marca = "▶ " if f["nombre"] == resaltar else "  "
        tabla.add_row(marca + f["nombre"], f"[{color}]{f['stock']}[/{color}]", str(f["minimo"]),
                      str(f["en_camino"]) if f["en_camino"] else "-",
                      style="bold yellow" if f["nombre"] == resaltar else None)
    consola.print(tabla)
