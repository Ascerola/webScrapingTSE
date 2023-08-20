import pandas as pd
from bs4 import BeautifulSoup
import requests

# Script para consultar TSE por cedula recibiendo datos por archivo xlsx

# Excel

xl = pd.ExcelFile("cedulas.xlsx")
df1 = xl.parse("Hoja1")



# Web Scraping

urlConsulta = 'https://servicioselectorales.tse.go.cr/chc/consulta_cedula.aspx'
urlPersona = 'https://servicioselectorales.tse.go.cr/chc/resultado_persona.aspx'
print(urlPersona, urlConsulta)

# Create an empty DataFrame to store all scraped data
all_data = pd.DataFrame()

# Loop through each row in the Excel file
for index, row in df1.iterrows():
    cedula = row['Cedula']

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

# Request to start a session with site
    with requests.session() as s:
        s.post(urlConsulta, data=payload)
        r = s.get(urlPersona)

    # Parsing HTML and finding element table
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find elements with the sp ecified IDs
    labels = ["Label8", "Label7", "Label9"]  # IDs for "Nombre Completo", "Fecha Nacimiento", and "Nacionalidad"
    data_dict = {"Cedula": cedula} # Add cedula to data dictionary

    for label_id in labels:
        label_element = soup.find("span", {"id": label_id})
        if label_element:
            label_text = label_element.text.strip()
            value_element = label_element.find_next("span")
            if value_element:
                value = value_element.text.strip()
                value = value.replace("Ă", "Ñ")
                data_dict[label_text] = value

    # Create a DataFrame from the new data
    new_data = pd.DataFrame([data_dict])

    # Load the existing Excel file if it exists, otherwise create a new DataFrame
    excel_filename = "scraped_data.xlsx"
    try:
        existing_data = pd.read_excel(excel_filename)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    # Append new data to the existing DataFrame
    updated_data = pd.concat([existing_data, new_data], ignore_index=True)

    # Save the updated DataFrame to the Excel file
    updated_data.to_excel(excel_filename, index=False)

    print(f"New data inserted and saved to '{excel_filename}'")






