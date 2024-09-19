import pykka
import csv

class SaveActor(pykka.ThreadingActor):
    def on_receive(self, message):
        resultados = message.get('resultados', "")
        if resultados:
            # Guardar en un archivo .txt
            with open('resultados.txt', 'w') as f:
                f.write(resultados)
            
            # Guardar en un archivo .csv
            with open('resultados.csv', 'w', newline='') as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(["Nombre del Producto", "Precio"])
                for producto in resultados:
                    writer.writerow([producto['nombre'], producto['precio']])
            
            return "Resultados guardados en resultados.txt y resultados.csv"
        return "No se encontraron resultados para guardar."
