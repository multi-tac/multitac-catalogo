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

# Unir ambos catálogos
unificados = pd.concat(
    [pasteur, venirvos],
    ignore_index=True
)

# Guardar resultado
unificados.to_excel(
    "productos_unificados.xlsx",
    index=False
)

print(
    f"Productos unificados: {len(unificados)}"
)
