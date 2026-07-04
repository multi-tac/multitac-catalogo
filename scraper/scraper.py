import requests
import csv
from bs4 import BeautifulSoup

url = "https://pasteur86.com/novedades/"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

productos = soup.select(".cbp-item.xpro-woo-product-grid-item")

with open("pasteur86_productos.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f, delimiter=";")

    writer.writerow([
        "Producto",
        "PrecioProveedor",
        "Imagen"
    ])

    for producto in productos:

        nombre = producto.select_one(".xpro-woo-product-grid-title")
        precio = producto.select_one(".woocommerce-Price-amount")
        imagen = producto.select_one("img")

        writer.writerow([
            nombre.get_text(strip=True) if nombre else "",
            precio.get_text(strip=True) if precio else "",
            imagen.get("src") if imagen else ""
        ])

print("Archivo generado correctamente")
