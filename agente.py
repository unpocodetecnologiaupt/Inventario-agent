"""
EVOLUCIÓN DE agente.py

Bitácora de este archivo, en el orden en que creció: 5 -> 6 -> 7 -> 8 -> 9.
El archivo final está en proyecto_final/agente.py
"""


# ============================================================================
# PASO 5 · Las instrucciones
# ============================================================================

# NUEVO ARCHIVO.


"""EL AGENTE: instrucciones + memoria + ciclo."""

INSTRUCCIONES = """Eres el encargado del inventario de una tienda. Tienes herramientas para consultar y modificar el inventario.

REGLAS:
- Usa siempre las herramientas. Nunca inventes cifras ni nombres de productos.
- Para registrar una venta: busca el producto, calcula el stock nuevo (stock actual menos lo vendido) y actualízalo.
- Si un producto se queda sin stock (0), envía una notificación al gerente para que lo revise. No inventes nombres ni cantidades.
- Para saber qué falta por pedir: revisa los productos con stock bajo. Pide solo los que tengan en_camino igual a 0.
- Cuando pidas un producto, ordena la cantidad necesaria para llegar al doble de su mínimo.
- Si te dicen que llegó una orden: busca su id en las órdenes y complétala.
- Si una herramienta te regresa un error, léelo y corrige tu siguiente paso.
- Al terminar, responde con un resumen corto de lo que hiciste."""


# ============================================================================
# PASO 6 · La memoria
# ============================================================================

# Agrega al final:


# ---------- PIEZA 4 · LA MEMORIA ----------
memoria = [{"role": "system", "content": INSTRUCCIONES}]


# ============================================================================
# PASO 7 · El ciclo
# ============================================================================

# A) Imports, hasta arriba, debajo del comentario inicial:


# import json
# from llm import chat
# from herramientas import TOOLS, ejecutar


# B) Al final del archivo:


# ---------- PIEZA 5 · EL CICLO ----------
def a_dict(msg):
    """Convierte la respuesta del modelo en un mensaje que podamos guardar en la memoria."""
    d = {"role": "assistant", "content": msg.content or ""}
    if msg.tool_calls:
        d["tool_calls"] = [{"id": t.id, "type": "function",
                            "function": {"name": t.function.name, "arguments": t.function.arguments}}
                           for t in msg.tool_calls]
    return d


def correr(pedido):
    memoria.append({"role": "user", "content": pedido})
    while True:
        respuesta = chat(memoria, TOOLS)              # 1. el LLM decide
        memoria.append(a_dict(respuesta))
        if not respuesta.tool_calls:                  # 2. no pidió herramientas: terminó
            print("🤖", respuesta.content)
            return
        for t in respuesta.tool_calls:                # 3. el harness ejecuta lo que pidió
            args = json.loads(t.function.arguments)
            print(f"🛠  {t.function.name}({args})")
            resultado = ejecutar(t.function.name, args)
            print("👀", resultado)
            memoria.append({"role": "tool", "tool_call_id": t.id,
                            "content": json.dumps(resultado, ensure_ascii=False)})
        # 4. vuelve arriba: el LLM lee los resultados y decide el siguiente paso


# ============================================================================
# PASO 8 · Conectar el panel
# ============================================================================

# A) Import arriba:


# from panel import mostrar_inventario


# B) Arriba de def a_dict:


MODIFICAN = ["actualizar_producto", "agregar_producto", "quitar_producto", "crear_orden_compra", "completar_orden"]


# C) En correr, justo después de print("👀", resultado):


# if t.function.name in MODIFICAN:
#                 mostrar_inventario(resaltar=args.get("nombre"))
