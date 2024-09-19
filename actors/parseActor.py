import pykka
from bs4 import BeautifulSoup

class ParseActor(pykka.ThreadingActor):
    def on_receive(self, message):
        html_content = message.get('html')
        url = message.get('url')
        
        # Parseo basado en el origen de la URL
        if 'mercadolibre.com.ar' in url:
            return self.parse_mercadolibre(html_content)
        elif 'garbarino.com' in url:
            return self.parse_garbarino(html_content)
        elif 'musimundo.com' in url:
            return self.parse_musimundo(html_content)
        else:
            return {'name': 'Unknown', 'price': None, 'source': 'Unknown'}

    def parse_mercadolibre(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            # Extraer el nombre del producto
            product_name = soup.find('h1').get_text().strip()
            
            # Extraer el precio del producto
            price = soup.find('span', class_='price-tag-fraction').get_text().replace('.', '')
            price = float(price)
            
            return {'name': product_name, 'price': price, 'source': 'MercadoLibre'}
        
        except Exception as e:
            return {'name': 'Unknown', 'price': None, 'source': 'MercadoLibre', 'error': str(e)}

    def parse_garbarino(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            # Extraer el nombre del producto
            product_name = soup.find('h1').get_text().strip()
            
            # Extraer el precio del producto
            price = soup.find('span', class_='value-item').get_text().replace('.', '')
            price = float(price)
            
            return {'name': product_name, 'price': price, 'source': 'Garbarino'}
        
        except Exception as e:
            return {'name': 'Unknown', 'price': None, 'source': 'Garbarino', 'error': str(e)}

    def parse_musimundo(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            # Extraer el nombre del producto
            product_name = soup.find('h1').get_text().strip()
            
            # Extraer el precio del producto
            price = soup.find('div', class_='product-price').find('span').get_text().replace('.', '')
            price = float(price)
            
            return {'name': product_name, 'price': price, 'source': 'Musimundo'}
        
        except Exception as e:
            return {'name': 'Unknown', 'price': None, 'source': 'Musimundo', 'error': str(e)}
