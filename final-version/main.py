from agente import correr
from agente import memoria
from panel import mostrar_inventario

if __name__ == "__main__":
    print("📦 Agente de inventario listo. Escribe 'salir' para terminar.\n")
    while True:
        mostrar_inventario()      # cómo está el inventario antes
        pedido = input("🧑 Tú: ").strip()
        if pedido.lower() in ("salir", "exit"):
            break
        if pedido:
            correr(pedido)
            print(f"💾 memoria: {len(memoria)} mensajes\n")
