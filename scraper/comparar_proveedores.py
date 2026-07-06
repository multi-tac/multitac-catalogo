import pandas as pd

# ======================
# PASTEUR
# ======================

pasteur = pd.read_csv(
    "multitac_productos.csv",
    sep=";"
)

pasteur["Proveedor"] = "PASTEUR"
pasteur["Usar"] = ""

# ======================
# VENIRVOS
# ======================

venirvos = pd.read_excel(
    "venirvos.xlsx"
)

venirvos["Proveedor"] = "VENIRVOS"
venirvos["Usar"] = ""

# ======================
# CREAR SUBCATEGORIA SI NO EXISTE
# ======================

if "Subcategoria" not in pasteur.columns:
    pasteur["Subcategoria"] = ""

if "Subcategoria" not in venirvos.columns:
    venirvos["Subcategoria"] = ""

# ======================
# UNIFICAR
# ======================

unificados = pd.concat(
    [pasteur, venirvos],
    ignore_index=True
)

# ======================
# SUBCATEGORIZAR
# ======================

def obtener_subcategoria(nombre):

    nombre = str(nombre).upper()

    # ---- CUCHILLERIA ----

    if any(x in nombre for x in [
        "CUCHILLO",
        "KNIFE",
        "DAGA",
        "DAGGER",
        "PUÑAL",
        "PUNAL",
        "PUSH",
        "BAYONETA",
        "EXPERIENCE"
    ]):
        return "CUCHILLOS"

    elif "NAVAJA" in nombre:
        return "NAVAJAS"

    elif "MACHETE" in nombre:
        return "MACHETES"

    elif "HACHA" in nombre or "HACHUELA" in nombre:
        return "HACHAS"

    elif "KERAMBIT" in nombre:
        return "KERAMBIT"

    elif "MARIPOSA" in nombre:
        return "MARIPOSAS"

    elif "MULTIUSO" in nombre:
        return "HERRAMIENTA"

    # ---- CAMPING ----

    elif "LINTERNA" in nombre or "FAROL" in nombre:
        return "LINTERNAS"

    elif any(x in nombre for x in [
        "ENCENDEDOR",
        "PEDERNAL"
    ]):
        return "ENCENDEDORES"

    elif "CARPA" in nombre:
        return "CARPAS"

    elif any(x in nombre for x in [
        "SLEEPING",
        "AISLANTE",
        "TOLDO",
        "TARP"
    ]):
        return "CARPAS"

    elif any(x in nombre for x in [
        "MULTIHERRAMIENTA",
        "MULTIFUNCION",
        "MULTIFUNCIÓN",
        "MULTITOOL"
    ]):
        return "HERRAMIENTA"

    elif "MASCARILLA" in nombre or "RCP" in nombre:
        return "BUFF"

    elif "CONSERVADORA" in nombre:
        return "HERRAMIENTA"

    elif "WALKIE" in nombre:
        return "HERRAMIENTA"

    # ---- INDUMENTARIA ----

    elif "GUANTE" in nombre:
        return "GUANTES"

    elif "CHALECO" in nombre or "PECHERA" in nombre:
        return "CHALECOS"

    elif any(x in nombre for x in [
        "MOCHILA",
        "MORRAL",
        "BANDOLERA",
        "SOBAQUERA"
    ]):
        return "MOCHILAS"

    elif any(x in nombre for x in [
        "GORRA",
        "SOMBRERO",
        "BALACLAVA",
        "BANDANA"
    ]):
        return "GORROS"

    elif "RELOJ" in nombre:
        return "RELOJES"

    elif "BUFF" in nombre or "CUELLO" in nombre:
        return "BUFF"

    elif any(x in nombre for x in [
        "PROTECTORES",
        "AUDITIVOS",
        "PARAGUAS"
    ]):
        return "HERRAMIENTA"

    # ---- ACCESORIOS ----

    elif "MOSQUETON" in nombre or "MOSQUETÓN" in nombre:
        return "MOSQUETONES"

    elif "LLAVERO" in nombre:
        return "LLAVEROS"

    elif any(x in nombre for x in [
        "VIOLENT",
        "GAS DEFENSA",
        "MANOPLA",
        "BASTON",
        "BASTÓN",
        "NUNCHAKU",
        "KUBOTAN",
        "CORTACINTO"
    ]):
        return "DEFENSA"

    elif "REMACHADORA" in nombre:
        return "HERRAMIENTA"

    return ""

# ======================
# COMPLETAR SUBCATEGORIAS
# ======================

unificados["Subcategoria"] = unificados["Producto"].apply(
    obtener_subcategoria
)

# ======================
# ORDENAR COLUMNAS
# ======================

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

# ======================
# EXPORTAR
# ======================

unificados.to_excel(
    "productos_unificados.xlsx",
    index=False
)

print(
    f"✅ Productos unificados: {len(unificados)}"
)

sin_subcategoria = (
    unificados["Subcategoria"]
    .fillna("")
    .astype(str)
    .str.strip()
    .eq("")
    .sum()
)

print(
    f"✅ Productos sin subcategoría: {sin_subcategoria}"
)
print("VERSION NUEVA SUBCATEGORIAS")