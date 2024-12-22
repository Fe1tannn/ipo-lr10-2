import requests
from bs4 import BeautifulSoup
from bs4 import Tag
import json

list_country = []
list_capital = []
writer_list = []
file_json = "data.json"
file_template = "index.html"
file_index = "index.html"
url = 'https://www.scrapethissite.com/pages/simple/'

# Получаем html страницы
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
country = soup.find_all('h3', class_='country-name')
capital = soup.find_all('span', class_='country-capital')

for countr in country:
    list_country.append(countr.text.rstrip())

for cap in capital:
    list_capital.append(cap.text.rstrip())

for i in range(len(list_country)):
    print(f'''{i + 1}. Country: {list_country[i]}; Capital: {list_capital[i]};''')

with open(file_json, "w+", encoding='utf-8') as file:
    for i in range(len(list_country)):
        writer = {'Country': list_country[i], 'Capital': list_capital[i]}
        writer_list.append(writer)
    json.dump(writer_list, file, indent=5, ensure_ascii=False)

# Прочитать шаблон HTML
with open(file_template, 'r', encoding='utf-8') as file:
    filedata = file.read()

soup = BeautifulSoup(filedata, "html.parser")

# Найти элемент, куда будем добавлять новые данные
element_to_paste = soup.find("div", class_="place-here")

if element_to_paste is not None:
    table = Tag(name="table")
    table['cellspacing'] = "4"
    table['bordercolor'] = "purple"
    table['bgcolor'] = "#9163bf"
    table['border'] = "3"
    table['align'] = "center"

    header_row = Tag(name="tr")
    headers = ["Страна", "Столица", "Номер"]
    for header in headers:
        th = Tag(name="td")
        th.string = header
        header_row.append(th)
    table.append(header_row)

    with open(file_json, "r", encoding='utf-8') as input:
        data_writer = json.load(input)
        for i, item in enumerate(data_writer):
            new_row = Tag(name="tr")

            country_cell = Tag(name="td")
            country_cell.string = item['Country']
            new_row.append(country_cell)

            capital_cell = Tag(name="td")
            capital_cell.string = item['Capital']
            new_row.append(capital_cell)

            number_cell = Tag(name="td")
            number_cell.string = str(i + 1)
            new_row.append(number_cell)

            table.append(new_row)

    element_to_paste.append(table)

    # Сохранить измененный HTML в новый файл
    with open(file_index, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
else:
    print('Элемент с классом "place-here" не найден в шаблоне HTML.')
