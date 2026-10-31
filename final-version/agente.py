import json
from llm import chat
from herramientas import TOOLS, ejecutar

INSTRUCCIONES = """Eres el encargado del inventario de una tienda. Tienes herramientas para consultar y modificar el inventario.

REGLAS:
- Usa siempre las herramientas. Nunca inventes cifras ni nombres de productos.
- Para registrar una venta: busca el producto, calcula el stock nuevo (stock actual menos lo vendido) y actualízalo.
- Para saber qué falta por pedir: revisa los productos con stock bajo. Pide solo los que tengan en_camino igual a 0.
- Cuando pidas un producto, ordena la cantidad necesaria para llegar al doble de su mínimo.
- Si te dicen que llegó una orden: busca su id en las órdenes y complétala.
- Si una herramienta te regresa un error, léelo y corrige tu siguiente paso.
- Al terminar, responde con un resumen corto de lo que hiciste.
- Si un producto no tiene stock envia una notificación al gerente para que lo revise. No inventes nombres ni cantidades."""

memoria = [{"role": "system", "content": INSTRUCCIONES}]

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
        #print("🔁", "-"*40, "Inicia paso", "-"*40)
        respuesta = chat(memoria, TOOLS)              # 1. el LLM decide
        memoria.append(a_dict(respuesta))
        if not respuesta.tool_calls:                  # 2. no pidió herramientas: terminó
            print("🤖", respuesta.content)
            return
        for t in respuesta.tool_calls:                # 3. el harness ejecuta lo que pidió
            args = json.loads(t.function.arguments)
            #print(f"🛠  {t.function.name}({args})")
            resultado = ejecutar(t.function.name, args)
            #print("👀", resultado)
            memoria.append({"role": "tool", "tool_call_id": t.id,
                            "content": json.dumps(resultado, ensure_ascii=False)})
        #print("🔁", "-"*40, "Terminapaso", "-"*40)