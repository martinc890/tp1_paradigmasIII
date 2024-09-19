import pykka

class CompareActor(pykka.ThreadingActor):
    def on_receive(self, message):
        productos = message.get('productos', [])
        
        if not productos:
            return "No se recibieron productos para comparar."

        # Filtrar productos con precios válidos
        productos_validos = []
        for producto in productos:
            try:
                # Limpiar el precio y convertirlo a float
                precio_str = producto['precio'].replace('.', '').replace(',', '.').replace('$', '').strip()
                precio = float(precio_str)
                productos_validos.append({'nombre': producto['nombre'], 'precio': precio})
            except ValueError as e:
                print(f"Error procesando el precio de {producto['nombre']}: {e}")
                continue

        if not productos_validos:
            return "No se encontraron productos válidos para comparar."

        # Ordenar productos por precio
        productos_ordenados = sorted(productos_validos, key=lambda p: p['precio'])

        return productos_ordenados
