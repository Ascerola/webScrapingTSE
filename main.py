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
        '__VIEWSTATE': "/wEPDwUKMTE5NjQ0MTE0NGRkwADSeM+nCTL00mzElkyIfBMhLFMHXfD7G6CsB6Qd+10=",
        '__VIEWSTATEGENERATOR': "88BF6952",
        '__EVENTVALIDATION': "/wEdAAlu/BGTruKh2u/D9xnIhqgNtTfNpOz0CH4vKngBfzxDIS2hNtLCXCKq92TKMjYS4CX24YOX6Ab2AoRRJXYcN6RPZrHMfDaOuX2c5DuODJSeiypYaPycT+v9uchEvEhJB0tWvoSmUD9cccAzkkmmOR9zkJ/OtIbU04qfUHmBu0NaRFCfQQ61frM+tUgerGfanga847SEt7x78XyqJ89dXW1XSczdg0rUIuxTrK/JJDYwQA==",
        'txtcedula': cedula,
        '__ASYNCPOST': "True",
        'btnConsultaCedula': 'Consultar'
    }

    with requests.session() as s:
        s.post(urlConsulta, data=payload)
        r = s.get(urlPersona)

    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the link to "Ver Más Detalles"
    ver_mas_link = soup.find("a", {"id": "LinkButton11"})

    if ver_mas_link:
        ver_mas_href = ver_mas_link.get("href")
        ver_mas_payload = {
            'ScriptManager1': 'UpdatePanel4|LinkButton11',
            '__EVENTTARGET': 'LinkButton11',
            '__VIEWSTATE': '/wEPDwULLTE1NTg5MDEzMzIPZBYCAgUPZBYKAg0PZBYCZg9kFiYCAw8PFgQeBFRleHQFJ1NPTElDSVRBUiBDRVJUSUZJQ0FDSU9OIERFIEVTVEFETyBDSVZJTB4HVG9vbFRpcAUnU09MSUNJVEFSIENFUlRJRklDQUNJT04gREUgRVNUQURPIENJVklMZGQCCQ8PFgIeB1Zpc2libGVoZGQCDQ8PFgIfAmhkZAITDw8WAh8ABQkxMTcxMDA1OTFkZAIXDw8WAh8ABQoxNC8wNS8xOTk4ZGQCGw8PFgIfAAUfRVJJQ0sgREFOSUVMIFZJTExBTE9CT1MgIE1Vw5FPWmRkAh8PDxYCHwAFDUNPU1RBUlJJQ0VOU0VkZAIjDw8WAh8ABQEgZGQCJw8PFgIfAAUIMjUgQcORT1NkZAIrDw8WAh8ABRhFUklDSyBWSUxMQUxPQk9TIEFMVkFSRVpkZAIvDw8WAh8ABQJOT2RkAjMPDxYCHwAFCTIwNDc3MDE1NmRkAjsPDxYCHwAFFEFEUklBTkEgTVXDkU9aIEdPTUVaZGQCQQ8PFgIfAAUJNjAyNTcwODgzZGQCQw8PFgIfAAUJU09MVEVSTy9BZGQCRQ8PFgIfAAUCMTBkZAJJDw8WAh8AZWRkAk0PDxYCHwAFCU1BU0NVTElOT2RkAk8PDxYCHwBlZGQCHw8PFgIfAGVkZAInD2QWAmYPZBYCAgMPPCsAEQIBEBYAFgAWAAwUKwAAZAIpD2QWAmYPZBYCAgMPPCsAEQIBEBYAFgAWAAwUKwAAZAIrD2QWAmYPZBYCAgMPPCsAEQIBEBYAFgAWAAwUKwAAZBgEBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBAULSW1hZ2VJbmljaW8FE0ltYWdlQ29uc3VsdGFDZWR1bGEFE0ltYWdlQ29uc3VsdGFOb21icmUFCkltYWdlU2FsaXIFDEdyaWR2b3RhY2lvbg9nZAUPR3JpZG1hdHJpbW9uaW9zD2dkBQlHcmlkaGlqb3MPZ2SbnpFpICKAvElWYlVXy4/QoGgfdXA03oaRbKW9Q0RTng==',
            '__VIEWSTATEGENERATOR': '9B2EA161',
            '__EVENTVALIDATION': '/wEdABHZtkNMCu/OIz70ETufZeU4iqbymbVNf9U++jDqKpBZeKfpigIS2tjkEVbbLpJMXRKuK+c1zGEqN0QiOtSVIjbTo8XTvMemOeiTsiCv52YIemVikE++yEdoHTLugZV7sMg9MKWwyYnyGaRupuuiPjUTpRd+w+p8QgmIF/xj83k64/we9+BwVz5Ihp+bC78EPFMCfHJxCCGkqx0cEcFZIWbctTfNpOz0CH4vKngBfzxDIS2hNtLCXCKq92TKMjYS4CX24YOX6Ab2AoRRJXYcN6RPb/5cgUWoPLK9FRe9Wehz9MYrrw85uciTs0i4KdeN/lBd3VPD6Wym8us3eHD1WYbKZrHMfDaOuX2c5DuODJSeixc/W2v/1estRMpOYE4jubza9ta9DzA1yI1treg4LQu1',
            'hdnCodigoAccionMarginal': '1',
            '__ASYNCPOST': "True"
        }

        # Send a postback request to the "Ver Más Detalles" link
        r_ver_mas = s.post(urlPersona, data=ver_mas_payload)

        # Parse the new page content
        soup_ver_mas = BeautifulSoup(r_ver_mas.content, 'html.parser')

        labels = ["Label1", "Label2", "Label3", "Label8", "Label12", "Label9"]  # Update with actual label IDs
        data_dict = {"Cedula": cedula}

        for label_id in labels:
            label_element = soup_ver_mas.find("span", {"id": label_id})
            if label_element:
                label_text = label_element.text.strip()
                value_element = label_element.find_next("span")
                if value_element:
                    value = value_element.text.strip()
                    value = value.replace("Ă", "Ñ")
                    data_dict[label_text] = value

        return pd.DataFrame([data_dict])

    return pd.DataFrame()


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