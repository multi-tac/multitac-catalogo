import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

BASE_URL = "https://venirvosj.com.ar"
GANANCIA = 35

productos = []

headers = {
    "User-Agent": "Mozilla/5.0"
}

page = 1

while True:

    url = f"{BASE_URL}/page/{page}"

    print(f"Procesando página {page}")

    r = requests.get(url, headers=headers, timeout=30)

    if r.status_code != 200:
        break

    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select("li.product")

    if not cards:
        break

    for card in cards:

        try:

            nombre_tag = card.select_one("h2")
            if not nombre_tag:
                continue

            nombre_original = nombre_tag.get_text(strip=True)

            sku = ""

            match = re.search(r"\(([^()]+)\)\s*$", nombre_original)

            if match:

                sku = match.group(1).strip()

            nombre = re.sub(r"\s*\([^()]+\)\s*$", "", nombre_original).strip()
            

            categoria_tag = card.select_one(".product-category")
            categoria = categoria_tag.get_text(strip=True).upper() if categoria_tag else ""

            precio_tag = card.select_one(".price")

            precio_texto = precio_tag.get_text(" ", strip=True) if precio_tag else ""

            numeros = re.findall(r"[\d\.]+", precio_texto)

            if numeros:
                precio = int(numeros[0].replace(".", ""))
            else:
                precio = 0

            precio_reventa = round(precio * (1 + GANANCIA / 100))

            link_tag = card.select_one("a")

            link_producto = (
                link_tag["href"]
                if link_tag and link_tag.has_attr("href")
                else ""
            )

            img_tag = card.select_one("img")

            imagen = ""

            if img_tag:
                imagen = (
                    img_tag.get("data-src")
                    or img_tag.get("src")
                    or ""
                )

            disponible = "SI"

            texto_card = card.get_text(" ", strip=True).upper()

            if "AGOTADO" in texto_card:
                disponible = "NO"
            nombre_upper = nombre.upper()

            if any(x in nombre_upper for x in [
                "CUCHILLO",
                "NAVAJA",
                "MACHETE",
                "KATANA",
                "KERAMBIT",
                "MARIPOSA"
            ]):
                categoria = "CUCHILLERIA"

            elif any(x in nombre_upper for x in [
                "CARPA",
                "MOSQUETON",
                "SOGA",
                "PULSERA",
                "SET CUBIERTO",
                "PANEL SOLAR"
            ]):
                categoria = "CAMPING"

            elif any(x in nombre_upper for x in [
                "CHALECO",
                "GUANTE",
                "CAMPERA",
                "REMERA",
                "PANTALON",
                "GORRA"
            ]):
                categoria = "INDUMENTARIA"

            elif "LINTERNA" in nombre_upper:
                categoria = "LINTERNA"

            elif any(x in nombre_upper for x in [
                "PINZA",
                "LLAVE",
                "DESTORNILLADOR",
                "HERRAMIENTA"
            ]):
                categoria = "HERRAMIENTA"

            elif any(x in nombre_upper for x in [
                "LED",
                "CABLE",
                "CARGADOR",
                "ELECTRICO",
                "ELECTRICA"
            ]):
                categoria = "ELECTRICOS"

            elif any(x in nombre_upper for x in [
                "TERMO",
                "MATE",
                "VASO",
                "TAZA",
                "JARRA"
            ]):
                categoria = "BAZAR"

            else:
                categoria = "ACCESORIOS"


            productos.append({
                "SKU": sku,
                "Producto": nombre,
                "Categoria": categoria,
                "PrecioProveedor": precio,
                "%Ganancia": GANANCIA,
                "PrecioReventa": precio_reventa,
                "Imagen": imagen,
                "Disponible": disponible
            })


        except Exception as e:
            print("Error:", e)

    page += 1
    time.sleep(1)

df = pd.DataFrame(productos)

df.to_excel("venirvos.xlsx", index=False)

print(f"Productos exportados: {len(df)}")