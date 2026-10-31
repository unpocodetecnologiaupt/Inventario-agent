# 📦 Mi primer agente · Inventario con un LLM local

Proyecto del video **"Mi primer agente"** del canal *Un Poco de Tecnología*.
Un agente de inventario para una tienda, hecho en Python con un modelo que corre en tu propia computadora (Ollama + Qwen).

> **Agente = LLM + harness.** El LLM decide qué hacer en cada paso. El harness (herramientas, instrucciones, memoria y ciclo) es todo lo que lo rodea.

---

## Qué hace

Le escribes en lenguaje natural y él decide qué herramientas usar y en qué orden:

- `Vendí 3 playeras negras` → busca el producto, calcula el stock nuevo y lo actualiza.
- `Vendí las 4 mochilas` → se queda en 0 y **avisa al gerente**.
- `¿Qué me falta por pedir? Haz las órdenes` → revisa el stock bajo y crea órdenes solo para lo que no tiene nada en camino.
- `Llegó la orden de las tazas` → completa la orden y suma las unidades al stock.

Cada vez que modifica algo, se redibuja una tabla del inventario en la terminal, con el producto afectado marcado.

## Requisitos

- Python 3.10 o superior (en Windows se usa `py`)
- [Ollama](https://ollama.com) corriendo, con un modelo descargado que soporte herramientas (el del video es Qwen)
- Librerías: `openai` y `rich`

```
py -m pip install -r requirements.txt
```

Abre `llm.py` y revisa que `MODELO` sea el nombre exacto que sale en `ollama list`.
Este proyecto asume el modelo con el razonamiento (`think`) desactivado.

## Cómo correrlo

```
py db.py        # crea/reinicia la base de datos (hazlo antes de cada toma)
py agente.py    # chat libre con el agente  ("salir" para terminar)
py main.py      # un pedido fijo, con la tabla antes y después
```

## Qué contiene cada archivo

| Archivo | Para qué sirve |
|---|---|
| `db.py` | Base de datos SQLite: 10 productos y una orden de 10 tazas ya en camino. |
| `llm.py` | Una función `chat()` que habla con Ollama usando la API compatible con OpenAI. |
| `herramientas.py` | Las 10 herramientas, cómo se las presentamos al modelo (`TOOLS`) y `ejecutar()`. |
| `agente.py` | Las instrucciones, la memoria, el ciclo y el arranque del chat. |
| `panel.py` | La tabla del inventario en la terminal. |
| `main.py` | Un pedido fijo para tomas y pruebas. |

## Las piezas del agente

1. **LLM** (`llm.py`): el modelo local. Decide el siguiente paso.
2. **Herramientas** (`herramientas.py`): funciones de Python que el modelo puede pedir. Él no las ejecuta: las pide, y el harness las corre.
3. **Instrucciones** (`agente.py`): el mensaje `system` con las reglas de trabajo.
4. **Memoria** (`agente.py`): la lista `memoria`. El modelo no recuerda nada por sí solo; en cada llamada se le manda la lista completa.
5. **Ciclo** (`agente.py`, función `correr`): el modelo decide → el harness ejecuta la herramienta → el resultado vuelve a la memoria → el modelo decide otra vez, hasta que ya no pide más herramientas.

### Los roles de la memoria

| Rol | Quién habla |
|---|---|
| `system` | Tú: las instrucciones. Va al inicio de la lista. |
| `user` | La persona que usa el agente. |
| `assistant` | El modelo: sus respuestas y las herramientas que pide. |
| `tool` | El resultado de una herramienta. |

## Las 10 herramientas

| Herramienta | Qué hace |
|---|---|
| `listar_productos` | Todos los productos con stock, mínimo y costo. |
| `buscar_producto` | Busca por nombre y regresa el stock actual. |
| `agregar_producto` | Da de alta un producto nuevo. |
| `quitar_producto` | Elimina un producto. |
| `actualizar_producto` | Cambia stock, mínimo o costo. El stock es el valor **nuevo**, no una resta. |
| `listar_stock_bajo` | Productos en o bajo su mínimo, con las unidades `en_camino`. |
| `crear_orden_compra` | Crea una orden para reponer un producto. |
| `listar_ordenes` | Lista las órdenes (opcional: por estado). |
| `completar_orden` | Marca una orden como recibida y suma las unidades al stock. |
| `notificar_gerente` | Avisa al gerente (aquí solo se imprime; en la vida real sería correo, WhatsApp o Slack). |

## Frases para la demo

Antes de cada toma: `py db.py` y luego `py agente.py`.

1. `¿Qué productos tengo en el inventario?`
2. `Vendí 3 playeras negras y 2 sudaderas grises`
3. `Vendí las 4 mochilas`
4. `¿Qué me falta por pedir? Haz las órdenes`
5. `¿Y de la taza qué pasó?`
6. `Llegó la orden de las tazas`

Extra: `Agrega un producto nuevo: Cartera, 6 piezas, mínimo 3, costo 200` y `Quita el llavero del inventario`.

Es un modelo local: puede variar un poco de una corrida a otra.

## Carpeta `evolucion/`

Un `.py` por cada archivo del proyecto, con los bloques en el orden en que se fue agregando y cambiando durante el video (pasos 1 al 10). Son bitácoras para consultar: **no se ejecutan**. El proyecto funcional está en `proyecto_final/`.

## Notas

- Es una demo **happy path**: no tiene validaciones ni límites (por ejemplo, de gasto). Solo muestra cómo un LLM decide qué herramientas usar.
- No se guarda nada fuera de `inventario.db`, que se recrea con `py db.py`.
