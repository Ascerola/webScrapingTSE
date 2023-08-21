import pandas as pd
from bs4 import BeautifulSoup
import requests
import concurrent.futures

# Excel
xl = pd.ExcelFile("cedulas.xlsx")
df1 = xl.parse("Hoja1")

# Web Scraping
urlConsulta = 'https://servicioselectorales.tse.go.cr/chc/consulta_cedula.aspx'
urlPersona = 'https://servicioselectorales.tse.go.cr/chc/resultado_persona.aspx'

# Function to scrape data for a given cedula
def scrape_cedula(cedula):
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

    labels = ["Label8", "Label7", "Label9"]
    data_dict = {"Cedula": cedula}

    for label_id in labels:
        label_element = soup.find("span", {"id": label_id})
        if label_element:
            label_text = label_element.text.strip()
            value_element = label_element.find_next("span")
            if value_element:
                value = value_element.text.strip()
                value = value.replace("Ă", "Ñ")
                data_dict[label_text] = value

    return pd.DataFrame([data_dict])

# Number of threads/workers to use
num_workers = 5

# Create an empty DataFrame to store all scraped data
all_data = pd.DataFrame()

with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    # Use a list comprehension to submit tasks
    futures = [executor.submit(scrape_cedula, cedula) for cedula in df1['Cedula']]

    # Wait for all tasks to complete and retrieve results
    for future in concurrent.futures.as_completed(futures):
        try:
            new_data = future.result()
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
        except Exception as e:
            print(f"An error occurred: {e}")