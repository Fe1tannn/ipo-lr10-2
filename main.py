import requests  #Запросы в интернет
from bs4 import BeautifulSoup 
import json #Работа с json 
list_country = []  #Лист для хранения цитат
list_capital = [] #Лист для хранения авторов цитат
writer_list = [] #Общий лист цитаты + авторы
file_json = "data.json"  #Переменная для файла json
file_index = "index.html" #Создаваемая программой страница
url = 'https://www.scrapethissite.com/pages/simple/' #Сайт для парсинга информации

response = requests.get(url) #Получаем html страницы 
soup = BeautifulSoup(response.text, 'lxml') #Парсим информацию
country = soup.find_all('h3', class_='country-name') #Собираем все цитаты через тег h3/country-name
capital = soup.find_all('span', class_='country-capital') #Собираем всех авторов через тег span/country-capital
for countr in country: #Добавление стран в ранее созданный список
    list_country.append(countr.text.rstrip())  

for cap in capital:  #Добавление столиц в ранее созданный список
    list_capital.append(cap.text.rstrip())  

for i in range(len(list_country)):
    print(f'''{i + 1}. Country: {list_country[i]}; Capital: {list_capital[i]};''')
    
with open(file_json, "w+", encoding='utf-8') as file:  #Запись в json файл
    for i in range(len(list_country)):   
        writer = {'Country': list_country[i], 'Capital': list_capital[i]}
        writer_list.append(writer)
    json.dump(writer_list, file, indent = 5, ensure_ascii = False)

with open(file_index, "w+" , encoding='utf-8') as file:  #создание файла index.html
    file.write("<html><head><title>Quotes</title></head><body>\n")  #Титульник старницы
    file.write('<h1><p align="center" > <a href="https://www.scrapethissite.com/pages/simple/">Страны и столицы</h1></a></p>\n') #Текст над таблицей с гиперссылкой на оригинальный источник
    file.write('<body bgcolor="#341b4d">\n') #Цвет фона
    file.write('<table cellspacing="4"  bordercolor="purple"  BGCOLOR= #9163bf border="3" align="center" ') #Атрибуты таблицы цвет границ\заливка таблицы\толщина границ\выравнивание по центру
    file.write("<table>\n") #Создание таблицы
    file.write("<tr>\n")
    file.write(" <td>Страна</td>\n<td>Столица</td>\n<td>Номер</td>\n</tr>\n") #Заголовки старницы

    with open(file_json, "r", encoding='utf-8') as input:
        data_writer =  json.load(input) #Переменная считывающая информацию с файла json 
        for i in range(len(data_writer)): #Цикл для записи информации в таблицу
            file.write(f"<tr>\n<td>{data_writer[i]['Country']}</td>\n<td>{data_writer[i]['Capital']}</td>\n<td>{i+1}</td>\n")
    file.write("</table>\n") #Закрывающий тег таблицы
    file.write("</body></html>") #Закрывающий тег страницы
