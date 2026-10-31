"""
EVOLUCIÓN DE llm.py

Bitácora de este archivo: se crea una vez (paso 2) y ya no cambia.
"""


# ============================================================================
# PASO 2 · Crear llm.py (el LLM local)
# ============================================================================

# NUEVO ARCHIVO. El MODELO debe ser el nombre exacto de `ollama list`.


from openai import OpenAI
URL = "http://localhost:11434/v1"   # Ollama
MODELO = "qwen3.5"                  # nombre exacto de `ollama list`
cliente = OpenAI(base_url=URL, api_key="local")
def chat(mensajes, herramientas=None):
    args = {"model": MODELO, "messages": mensajes, "temperature": 0.1}
    if herramientas:
        args["tools"] = herramientas
    return cliente.chat.completions.create(**args).choices[0].message
