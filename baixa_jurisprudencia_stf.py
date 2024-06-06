import requests
from datetime import datetime, timedelta
import calendar
import json
from pathlib import Path

def days_in_year(year):
    return 365 + calendar.isleap(year)

# Dados de sessão
session = requests.Session()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
session.headers.update({'User-Agent': user_agent})
session.cookies.set("sortFilter", "date-asc", domain="jurisprudencia.stf.jus.br", path="/")

# Datas iniciais e finais da busca
start_date = datetime(1988, 10, 5)
end_date = datetime(1988, 12, 31)
last_date = datetime(2023, 12, 31)

total_hits = 0
hit_limit = 250

# Itera requisições por ano
while end_date <= last_date:
    from_string = start_date.strftime("%d%m%Y")
    to_string = end_date.strftime("%d%m%Y")
    page = 0
    hit_counter = hit_limit
    
    # Itera sobre paginador devido ao limite imposto pela ferramenta de busca
    while hit_counter >= hit_limit:
        page_index = page * hit_limit
        
        # Gera requisição com a busca 
        with open('query.json', 'r') as query_file: 
            json_query = query_file.read().replace('from_string',f'"{from_string}"').replace('to_string',f'"{to_string}"').replace('page_index',str(page_index))
        response = session.post("https://jurisprudencia.stf.jus.br/api/search/search", json=json.loads(json_query))
        response_json = response.json()
        
        # Parsing do resulta
        output_json = [hit['_source'] for hit in response_json['result']['hits']['hits']]
        hit_counter = len(output_json)
        total_hits += hit_counter
        page += 1
        
        # Salva resultado em arquivos JSON divididos por ano e paginador 
        output_dir = "resultados_busca"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        filename = f"./{output_dir}/jurisprudencia_{from_string}_{to_string}_{page}.json"
        with open(filename, 'w') as file:
            json.dump(output_json, file, indent=4, ensure_ascii=False)
        print(filename, hit_counter)

    # Incrementa data inicial e final da próxima busca
    start_date = end_date + timedelta(days=1)
    end_date = end_date + timedelta(days=days_in_year(start_date.year))

print("Total de resultados:", total_hits)
