import requests
import csv
from bs4 import BeautifulSoup

with open(
    "cuchilleria_completa_con_sku.csv",
    "w",
    newline="",
    encoding="utf-8"
) as salida:

    writer = csv.writer(salida, delimiter=";")

    writer.writerow([
        "SKU",
        "Producto",
        "PrecioProveedor",
        "Imagen",
        "URL"
    ])

    with open(
        "cuchilleria_completa.csv",
        "r",
        encoding="utf-8"
    ) as entrada:

        reader = csv.DictReader(entrada, delimiter=";")

        for fila in reader:

            sku = ""

            try:
                html = requests.get(fila["URL"], timeout=10).text

                soup = BeautifulSoup(html, "html.parser")

                texto = soup.get_text(" ", strip=True)

                pos = texto.find("SKU:")

                if pos != -1:
                    sku = texto[pos + 4:pos + 20].strip().split()[0]

            except:
                pass

            print(f"SKU: {sku} - {fila['Producto']}")

            writer.writerow([
                sku,
                fila["Producto"],
                fila["PrecioProveedor"],
                fila["Imagen"],
                fila["URL"]
            ])

print("Archivo generado correctamente")