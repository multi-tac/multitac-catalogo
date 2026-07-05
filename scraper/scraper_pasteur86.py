import requests
import csv
from bs4 import BeautifulSoup

categorias = {
    "CUCHILLERIA": {
        "url": "https://pasteur86.com/categoria-producto/cuchilleria/",
        "paginas": 9
    },
    "CAMPING": {
        "url": "https://pasteur86.com/categoria-producto/camping/",
        "paginas": 9
    },
    "INDUMENTARIA": {
        "url": "https://pasteur86.com/categoria-producto/indumentaria/",
        "paginas": 9
    },
    "ACCESORIOS": {
        "url": "https://pasteur86.com/categoria-producto/accesorios/",
        "paginas": 9
    }
}

with open(
    "multitac_productos.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f, delimiter=";")

    writer.writerow([
        "SKU",
        "Producto",
        "Categoria",
        "PrecioProveedor",
        "%Ganancia",
        "PrecioReventa",
        "Imagen",
        "Disponible"
    ])

    for categoria, datos in categorias.items():

        print(f"\nProcesando {categoria}")

        for pagina in range(1, datos["paginas"] + 1):

            if pagina == 1:
                url = datos["url"]
            else:
                url = f'{datos["url"]}page/{pagina}/'

            print(f"Página {pagina}")

            try:

                html = requests.get(
                    url,
                    timeout=15
                ).text

                soup = BeautifulSoup(
                    html,
                    "html.parser"
                )

                productos = soup.select(
                    ".cbp-item.xpro-woo-product-grid-item"
                )

                for producto in productos:

                    nombre = producto.select_one(
                        ".xpro-woo-product-grid-title"
                    )

                    precio = producto.select_one(
                        ".woocommerce-Price-amount"
                    )

                    imagen = producto.select_one("img")

                    link = producto.select_one(
                        "a[href]"
                    )

                    nombre_txt = (
                        nombre.get_text(strip=True)
                        if nombre else ""
                    )

                    precio_txt = (
                        precio.get_text(strip=True)
                        if precio else ""
                    )

                    imagen_txt = (
                        imagen.get("src")
                        if imagen else ""
                    )

                    sku = ""

                    try:

                        producto_html = requests.get(
                            link.get("href"),
                            timeout=15
                        ).text

                        producto_soup = BeautifulSoup(
                            producto_html,
                            "html.parser"
                        )

                        texto = producto_soup.get_text(
                            " ",
                            strip=True
                        )

                        pos = texto.find("SKU:")

                        if pos != -1:
                            sku = texto[
                                pos + 4:pos + 20
                            ].strip().split()[0]

                    except:
                        pass

                    writer.writerow([
                        sku,
                        nombre_txt,
                        categoria,
                        precio_txt,
                        "50",
                        "",
                        imagen_txt,
                        "SI"
                    ])

                    print(sku, nombre_txt)

            except Exception as e:
                print("ERROR:", e)

print("FINALIZADO")