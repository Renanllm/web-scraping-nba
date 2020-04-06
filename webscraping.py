import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

# Configurando url
url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PTS&dir=1"

# Definindo os campos e as labels que vamos utilizar

rankings = {
    '3points': {'field':'FG3M', 'label': '3PM'},
    'points': {'field':'PTS', 'label': 'PTS'},
    'assistants': {'field':'AST', 'label': 'AST'},
    'rebounds': {'field':'REB', 'label': 'REB'},
    'steals': {'field':'STL', 'label': 'STL'},
    'blocks': {'field':'BLK', 'label': 'BLK'},
}

top10ranking = {}

def build_rank(type_ranking):

    field = rankings[type_ranking]['field']
    label = rankings[type_ranking]['label']

    # Efetuando o click para mudança na tabela dinamica 

    driver.find_element_by_xpath(f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()

    # Coletando os dados
    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute("outerHTML")

    # Parsear o conteúdo HTML - BeaultifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Estruturar conteúdo em um Data Frame - Pandas
    df_full = pd.read_html( str(table) )[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    # Transformar os Dados em um Dicionario de dados proprio
    return df.to_dict('records')

# Configurando o browser para realizar operações sem exibição
option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

# Abrindo o browser
driver.get(url)
driver.implicitly_wait(10)

# Percorrendo cada chave do nosso ranking e adicionando no nosso dicionário
for k in rankings:
    top10ranking[k] = build_rank(k)

driver.quit()

# Converter e salvar em um arquivo JSON
with open('json/ranking.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(top10ranking, indent=4)
    jp.write(js)