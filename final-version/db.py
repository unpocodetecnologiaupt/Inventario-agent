"""Base de datos de ejemplo (SQLite). Ejecuta `python db.py` para reiniciar los datos."""
import os
import sqlite3

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventario.db")

# nombre, stock, minimo, costo por unidad
PRODUCTOS = [
    ("Playera negra", 5, 4, 120),
    ("Playera blanca", 12, 4, 120),
    ("Gorra azul", 8, 3, 90),
    ("Sudadera gris", 7, 6, 280),
    ("Taza de cerámica", 2, 5, 45),
    ("Termo 500 ml", 9, 3, 150),
    ("Mochila", 4, 2, 350),
    ("Cuaderno", 25, 10, 30),
    ("Pluma", 40, 15, 8),
    ("Llavero", 3, 8, 15),
]


def conectar():
    con = sqlite3.connect(RUTA)
    con.row_factory = sqlite3.Row
    return con


def crear():
    if os.path.exists(RUTA):
        os.remove(RUTA)
    con = conectar()
    con.executescript("""
        CREATE TABLE productos (
            id INTEGER PRIMARY KEY, nombre TEXT UNIQUE,
            stock INTEGER, minimo INTEGER, costo REAL);
        CREATE TABLE ordenes (
            id INTEGER PRIMARY KEY, producto_id INTEGER,
            cantidad INTEGER, total REAL, estado TEXT DEFAULT 'pendiente');
    """)
    con.executemany("INSERT INTO productos (nombre, stock, minimo, costo) VALUES (?,?,?,?)", PRODUCTOS)
    # La taza ya tiene una orden en camino: sirve para mostrar que el agente "no repite"
    con.execute("INSERT INTO ordenes (producto_id, cantidad, total) VALUES (5, 10, 450)")
    con.commit()
    con.close()
    print("✅ inventario.db listo")


if __name__ == "__main__":
    crear()