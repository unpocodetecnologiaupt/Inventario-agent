"""
EVOLUCIÓN DE main.py

Bitácora de main.py: es el archivo de PRUEBAS. Cada versión reemplaza a la anterior.
Correr: py db.py  y luego  py main.py
"""


# ============================================================================
# VERSIÓN 1 · Paso 3 · Prueba de las funciones
# ============================================================================


from herramientas import *

print(listar_productos())
print(buscar_producto('playera'))
print(listar_stock_bajo())


# ============================================================================
# VERSIÓN 2 · Paso 4 · Prueba de TOOLS y ejecutar
# ============================================================================

# Debe salir 7, el error de la herramienta falsa, la orden creada y el stock bajo (Taza con en_camino 10).


from herramientas import TOOLS, ejecutar

print(len(TOOLS))
print(ejecutar("herramienta_falsa", {}))
print(ejecutar("crear_orden_compra", {"nombre": "Sudadera gris", "cantidad": 7}))
print(ejecutar("listar_stock_bajo", {}))


# ============================================================================
# VERSIÓN 3 · Paso 4b/4d · Órdenes y aviso al gerente
# ============================================================================

# len(TOOLS) ahora es 10.


from herramientas import TOOLS, ejecutar

print(len(TOOLS))
print(ejecutar("listar_ordenes", {}))
print(ejecutar("completar_orden", {"id": 1}))
print(ejecutar("buscar_producto", {"texto": "taza"}))   # stock: 2 -> 12
print(ejecutar("notificar_gerente", {"mensaje": "Mochila sin stock, favor de revisarla."}))


# ============================================================================
# VERSIÓN 4 · Paso 5 · Prueba de las instrucciones
# ============================================================================


from llm import chat
from agente import INSTRUCCIONES

mensajes = [
    {"role": "system", "content": INSTRUCCIONES},
    {"role": "user", "content": "¿Qué haces y cómo trabajas?"},
]
print(chat(mensajes).content)


# ============================================================================
# VERSIÓN 5 · Paso 6 · Prueba de la memoria
# ============================================================================

# Debe decir "5 mensajes en memoria" y saber que te llamas Luis.


from llm import chat
from agente import memoria

memoria.append({"role": "user", "content": "Hola, me llamo Luis"})
r = chat(memoria)
memoria.append({"role": "assistant", "content": r.content})
print(r.content)

memoria.append({"role": "user", "content": "¿Cómo me llamo?"})
r = chat(memoria)
memoria.append({"role": "assistant", "content": r.content})
print(r.content)

print(len(memoria), "mensajes en memoria")


# ============================================================================
# VERSIÓN 6 · Paso 7 · Primera corrida del ciclo
# ============================================================================


from agente import correr

correr("¿Cuánto stock tengo de playeras?")


# ============================================================================
# VERSIÓN 7 · Paso 7 · Pedido más largo (más pasos)
# ============================================================================


from agente import correr

# ============================================================================
# VERSIÓN 7 · Paso 8 · ARRANQUE: chatea con el agente
# ============================================================================

if __name__ == "__main__":
    print("📦 Agente de inventario listo. Escribe 'salir' para terminar.\n")
    while True:
        pedido = input("🧑 Tú: ").strip()
        if pedido.lower() in ("salir", "exit"):
            break
        if pedido:
            correr(pedido)
            print(f"💾 memoria: {len(memoria)} mensajes\n")

correr("Vendí 3 playeras negras, 2 sudaderas grises y las 4 mochilas. Después revisa qué falta por pedir y haz las órdenes.")


# ============================================================================
# VERSIÓN 8 · Paso 10 · FINAL (con el panel antes y después)
# ============================================================================


from agente import correr
from panel import mostrar_inventario

mostrar_inventario()      # cómo está el inventario antes

correr("Vendí 3 playeras negras, 2 sudaderas grises y las 4 mochilas. Después revisa qué falta por pedir y haz las órdenes.")

mostrar_inventario()      # cómo quedó al final


