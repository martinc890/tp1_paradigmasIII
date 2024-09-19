from actors.searchActor import SearchActor
import pykka

def main():
    # URLs específicas para scraping buscando "Samsung A24"
    urls = [
        "https://www.musimundo.com/search/?text=samsung+a15",
        "https://listado.mercadolibre.com.ar/samsung-a15#D[A:samsung]",
        "https://www.fravega.com/l/?keyword=samsung+a15",
        "https://www.amazon.com/s?k=samsung+a15"
    ]

    # Crear los actores
    search_actors = [SearchActor.start() for _ in urls]

    # Ejecutar la búsqueda en paralelo para cada URL
    for i, url in enumerate(urls):
        print(f"Scraping en URL: {url}")
        result = search_actors[i].ask({'url': url})  # Pasar la URL al SearchActor
        print(f"Resultados para {url}:\n{result}\n")

    # Detener los actores al finalizar
    pykka.ActorRegistry.stop_all()

if __name__ == "__main__":
    main()