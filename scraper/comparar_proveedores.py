import pandas as pd

# IMPORT_PASTEUR
pasteur = pd.read_csv(
    "multitac_productos.csv",
    sep=";"
)

pasteur["Proveedor"] = "PASTEUR"
pasteur["Usar"] = ""

# VENIRVOS
venirvos = pd.read_excel(
    "venirvos.xlsx"
)

venirvos["Proveedor"] = "VENIRVOS"
venirvos["Usar"] = ""

# Crear columna Subcategoria si no existe
if "Subcategoria" not in pasteur.columns:
    pasteur["Subcategoria"] = ""

if "Subcategoria" not in venirvos.columns:
    venirvos["Subcategoria"] = ""

# Unir ambos catálogos
unificados = pd.concat(
    [pasteur, venirvos],
    ignore_index=True
)

# Función para clasificar
def obtener_subcategoria(nombre):

    nombre = str(nombre).upper()

    if "NAVAJA" in nombre:
        return "NAVAJAS"

    elif "CUCHILLO" in nombre:
        return "CUCHILLOS"

    elif "MACHETE" in nombre:
        return "MACHETES"

    elif "HACHA" in nombre or "HACHUELA" in nombre:
        return "HACHAS"

    elif "KERAMBIT" in nombre:
        return "KERAMBIT"

    elif "MARIPOSA" in nombre:
        return "MARIPOSAS"

    elif "LINTERNA" in nombre or "FAROL" in nombre:
        return "LINTERNAS"

    elif "CARPA" in nombre:
        return "CARPAS"

    elif "MOCHILA" in nombre or "MORRAL" in nombre:
        return "MOCHILAS"

    elif "GUANTE" in nombre:
        return "GUANTES"

    elif "CHALECO" in nombre:
        return "CHALECOS"

    elif "MOSQUETON" in nombre:
        return "MOSQUETONES"

    elif "LLAVERO" in nombre:
        return "LLAVEROS"

    elif "ENCENDEDOR" in nombre:
        return "ENCENDEDORES"

    elif any(x in nombre for x in [
        "GAS DEFENSA",
        "MANOPLA",
        "BASTON",
        "BASTÓN",
        "NUNCHAKU",
        "KUBOTAN"
    ]):
        return "DEFENSA"

    return ""

# Completar Subcategoria automáticamente
unificados["Subcategoria"] = unificados["Producto"].apply(
    obtener_subcategoria
)
# Reordenar columnas
columnas = [
    "SKU",
    "Producto",
    "Categoria",
    "Subcategoria",
    "PrecioProveedor",
    "%Ganancia",
    "PrecioReventa",
    "Imagen",
    "Disponible",
    "Proveedor",
    "Usar"
]

unificados = unificados[columnas]

# Guardar resultado
unificados.to_excel(
    "productos_unificados.xlsx",
    index=False
)

print(
    f"Productos unificados: {len(unificados)}"
)