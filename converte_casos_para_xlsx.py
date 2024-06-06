import os, json
from openpyxl import Workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

directory = 'resultados_busca'
 
wb = Workbook()
ws = wb.active
for filename in os.listdir(directory):
    full_path = os.path.join(directory, filename)
    if os.path.isfile(full_path):
        with open(full_path, 'r') as cases_file:
            for case in json.load(cases_file):
                ws.append([case['id'], case['titulo'], case['julgamento_data'], ILLEGAL_CHARACTERS_RE.sub(r'',case['ementa_texto'])]+case['ministro_facet'])

wb.save("casos.xlsx")