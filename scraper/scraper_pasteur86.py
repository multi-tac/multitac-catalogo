import time
import requests
import csv
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://pasteur86.com"

# Headers de navegador real. Muchos WAFs (Cloudflare, Sucuri, etc.)
# bloquean o cortan en silencio requests con el User-Agent por
# defecto de curl/requests ("python-requests/x.y", "curl/8.x").
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}

session = requests.Session()
session.headers.update(HEADERS)


def get_con_reintentos(url, timeout=15, intentos=3, espera=3):
    """
    GET con headers de navegador y reintentos con backoff.
    Ayuda quando el WAF del sitio corta la conexión de forma
    intermitente (timeouts esporádicos) en vez de bloquear
    siempre.
    """
    ultimo_error = None
    for intento in range(1, intentos + 1):
        try:
            return session.get(url, timeout=timeout)
        except requests.exceptions.RequestException as e:
            ultimo_error = e
            print(f"  Intento {intento}/{intentos} falló para {url}: {e}")
            if intento < intentos:
                time.sleep(espera * intento)
    raise ultimo_error

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


def extraer_imagen(producto):
    """
    Devuelve la URL real de la imagen de un producto, aunque el tema
    use lazy-loading (data-src / data-lazy-src / srcset) en vez de
    poner la URL directamente en 'src'.
    """

    imagen = producto.select_one("img")

    if not imagen:
        return ""

    # Atributos donde los plugins de lazy-load suelen guardar la URL real,
    # en orden de prioridad.
    candidatos = [
        "data-lazy-src",
        "data-src",
        "data-original",
        "src",
    ]

    url = ""

    for attr in candidatos:
        valor = imagen.get(attr)
        if valor and not valor.strip().startswith("data:image"):
            url = valor.strip()
            break

    # Si lo único que hay es un srcset, tomamos la primera URL de ahí.
    if not url:
        for attr in ("data-lazy-srcset", "data-srcset", "srcset"):
            srcset = imagen.get(attr)
            if srcset:
                primera = srcset.split(",")[0].strip().split(" ")[0]
                if primera:
                    url = primera
                    break

    if not url:
        return ""

    # Completar URLs relativas (//host/... o /wp-content/...)
    url = urljoin(BASE_URL, url)

    return url


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

                html = get_con_reintentos(
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

                    precio_numerico = 0

                    if precio_txt:

                        solo_numeros = re.sub(
                            r"[^\d]",
                            "",
                            precio_txt
                        )

                        if solo_numeros:
                            precio_numerico = int(
                                solo_numeros
                            )

                    precio_reventa = round(
                        precio_numerico * 1.35
                    )

                    imagen_txt = extraer_imagen(producto)

                    # Si en la grilla no se pudo resolver la imagen
                    # (por ejemplo lazy-load agresivo), como último
                    # recurso la buscamos en la página del producto.
                    producto_soup = None

                    if link and link.get("href"):
                        try:
                            producto_html = get_con_reintentos(
                                link.get("href"),
                                timeout=15
                            ).text

                            producto_soup = BeautifulSoup(
                                producto_html,
                                "html.parser"
                            )
                        except Exception:
                            producto_soup = None

                    if not imagen_txt and producto_soup is not None:
                        img_producto = producto_soup.select_one(
                            ".woocommerce-product-gallery__image img, "
                            "img.wp-post-image"
                        )
                        if img_producto:
                            imagen_txt = (
                                img_producto.get("data-lazy-src")
                                or img_producto.get("data-src")
                                or img_producto.get("src")
                                or ""
                            )
                            if imagen_txt:
                                imagen_txt = urljoin(BASE_URL, imagen_txt.strip())

                    sku = ""

                    if producto_soup is not None:
                        try:
                            texto = producto_soup.get_text(
                                " ",
                                strip=True
                            )

                            pos = texto.find("SKU:")

                            if pos != -1:

                                sku = texto[
                                    pos + 4:pos + 20
                                ].strip().split()[0]
                        except Exception:
                            pass

                    writer.writerow([
                        sku,
                        nombre_txt,
                        categoria,
                        precio_numerico,
                        "35",
                        precio_reventa,
                        imagen_txt,
                        "SI"
                    ])

                    print(
                        sku,
                        nombre_txt,
                        precio_numerico,
                        precio_reventa,
                        imagen_txt
                    )

            except Exception as e:

                print(
                    "ERROR:",
                    e
                )

print("FINALIZADO")
