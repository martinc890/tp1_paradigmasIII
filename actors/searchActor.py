import pykka
import requests
from bs4 import BeautifulSoup

class SearchActor(pykka.ThreadingActor):
    def on_receive(self, message):
        url = message.get('url')
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                sopa = BeautifulSoup(respuesta.content, "html.parser")

                # Buscar los productos según la tienda
                productos = []
                if "musimundo" in url:
                    productos = sopa.find_all('div', class_='mus-product-box')
                elif 'mercadolibre' in url:
                    productos = sopa.find_all('li', class_='ui-search-layout__item')
                elif 'fravega' in url:
                    productos = sopa.find_all('article', class_='sc-812c6cb5-2')
                elif 'garbarino' in url:
                    productos = sopa.find_all('a', class_='card-anchor header')

                resultados = []

                for producto in productos:
                    # Para Musimundo
                    if "musimundo" in url:
                        h3 = producto.find('h3', class_='mus-pro-name')
                        nombre = h3.text.strip() if h3 else 'Título no encontrado'
                        span_tag = producto.find('span', class_='mus-pro-price-number')
                        precio = span_tag.text.strip() if span_tag else 'Precio no encontrado'

                    # Para MercadoLibre
                    elif 'mercadolibre' in url:
                        nombre_tag = producto.find('h2', class_='ui-search-item__title')
                        nombre = nombre_tag.text.strip() if nombre_tag else 'Título no encontrado'
                        precio_tag = producto.find('span', class_='price-tag-fraction')
                        precio = precio_tag.text.strip() if precio_tag else 'Precio no encontrado'

                    # Para Fravega
                    elif 'fravega' in url:
                        nombre_tag = producto.find('span', class_='sc-ca346929-0')
                        nombre = nombre_tag.text.strip() if nombre_tag else 'Título no encontrado'
                        precio_tag = producto.find('span', class_='sc-1d9b1d9e-0')
                        precio = precio_tag.text.strip() if precio_tag else 'Precio no encontrado'

                    # Para Garbarino
                    elif 'garbarino' in url:
                        nombre_tag = producto.find('div', class_='product-card-design6-vertical__name')
                        nombre = nombre_tag.text.strip() if nombre_tag else 'Título no encontrado'
                        precio_tag = producto.find('div', class_='product-card-design6-vertical__price')
                        precio_span = precio_tag.find_all('span')[-1].text.strip() if precio_tag else 'Precio no encontrado'

                    # Guardar el resultado sin filtrar
                    resultados.append(f"{nombre}: {precio}")

                if resultados:
                    return "\n".join(resultados)
                else:
                    return "No se encontró información del producto."
            else:
                return f"Error al acceder a {url}: {respuesta.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
