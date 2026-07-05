import csv
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

worksheet = sheet.worksheet("Hoja 1")

worksheet.clear()

with open(
    "multitac_productos.csv",
    encoding="utf-8"
) as archivo:

    datos = list(
        csv.reader(
            archivo,
            delimiter=";"
        )
    )

worksheet.update(datos)

print("Google Sheets actualizado correctamente")