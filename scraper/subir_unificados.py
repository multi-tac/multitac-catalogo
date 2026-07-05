import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file(
    "scraper/credenciales.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open_by_key(
    "1_odj6wFfsVmf7cADgHY5mHeGxvrxCA80ELHOlSDC_58"
)

worksheet = sheet.worksheet(
    "PRODUCTOS_UNIFICADOS"
)

worksheet.clear()

df = pd.read_excel(
    "productos_unificados.xlsx"
)

datos = [df.columns.tolist()] + df.fillna("").values.tolist()

worksheet.update(datos)

print(
    "PRODUCTOS_UNIFICADOS actualizado"
)