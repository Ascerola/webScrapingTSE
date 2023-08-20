import pandas as pd
from openpyxl import Workbook
from bs4 import BeautifulSoup
import requests

# Script para consultar TSE por cedula recibiendo datos por archivo xlsx#


# Excel#

xl = pd.ExcelFile("cedulas.xlsx")
df = xl.parse("Hoja1")
cedula = df['Cedula'][0]

# Web Scraping#

urlConsulta = 'https://servicioselectorales.tse.go.cr/chc/consulta_cedula.aspx'
urlPersona = 'https://servicioselectorales.tse.go.cr/chc/resultado_persona.aspx'
print(urlPersona, urlConsulta)
payload = {
    'ScriptManager1': 'UpdatePanel1|btnConsultaCedula',
    '__LASTFOCUS': "",
    '__EVENTTARGET': "",
    '__EVENTARGUMENT': "",
    '__VIEWSTATE': "/wEPDwUKMTE5NjQ0MTE0NGRkwADSeM+nCTL00mzElkyIfBMhLFMHXfD7G6CsB6Qd+10=",
    '__VIEWSTATEGENERATOR': "88BF6952",
    '__EVENTVALIDATION': "/wEdAAlu/BGTruKh2u/D9xnIhqgNtTfNpOz0CH4vKngBfzxDIS2hNtLCXCKq92TKMjYS4CX24YOX6Ab2AoRRJXYcN6RPZrHMfDaOuX2c5DuODJSeiypYaPycT+v9uchEvEhJB0tWvoSmUD9cccAzkkmmOR9zkJ/OtIbU04qfUHmBu0NaRFCfQQ61frM+tUgerGfanga847SEt7x78XyqJ89dXW1XSczdg0rUIuxTrK/JJDYwQA==",
    'txtcedula': cedula,
    'grupo': "",
    'comentario': "",
    '__ASYNCPOST': "True",
    'btnConsultaCedula': 'Consultar'
}

with requests.session() as s:
    s.post(urlConsulta, data=payload)
    r = s.get(urlPersona)
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify()) #
    table = soup.find('table', id="TABLE1")

    for row in table.find_all("tr"):
        row_data = []
        for cell in row.find_all(["th", "td"]):
            row_data.append(cell.get_text(strip=True))
        print(" | ".join(row_data))



