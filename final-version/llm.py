from openai import OpenAI

URL = "http://localhost:11434/v1" 
MODELO = "qwen3.5:9b"

cliente = OpenAI(base_url=URL, api_key="local")

def chat(mensajes, herramientas=None):
    """Envía la conversación al modelo y regresa su mensaje (texto y/o llamadas a herramientas)."""
    args = {"model": MODELO, "messages": mensajes, "temperature": 0.8}
    if herramientas:
        args["tools"] = herramientas
    return cliente.chat.completions.create(**args).choices[0].message