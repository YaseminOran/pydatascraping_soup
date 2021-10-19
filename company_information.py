import requests
from bs4 import BeautifulSoup
from lxml import etree, html
import json

url = 'https://finans.mynet.com/borsa/hisseler'

companies_html_data = []
website_content = requests.get(url).text
bs4 = BeautifulSoup(website_content, 'html.parser')
# Capture the table
table = bs4.find('table')
# Capture the `tbody`
table_body = table.find('tbody')

def get_company_data(html_data):
    data_parser = BeautifulSoup(html_data, 'html.parser')
    dom = etree.HTML(str(data_parser))
    xpath_query_initial ='//section/div[1]/div[1]/div[3]/div/div[1]/div[3]/div[2]/ul/li/span[2]'


    for index in range(len(dom.xpath(xpath_query_initial))):
        data = {
            "name": data_parser.find('h2').get_text(),
            "Hissenin ilk işlem tarihi": dom.xpath(xpath_query_initial)[0].text,
            "Son İşlem Fiyatı": dom.xpath(xpath_query_initial)[1].text,
            "Alış": dom.xpath(xpath_query_initial)[2].text,
            "Satış": dom.xpath(xpath_query_initial)[3].text,
            "Günlük Değişim": dom.xpath(xpath_query_initial)[4].text,
            "Günlük Değişim (%)": dom.xpath(xpath_query_initial)[5].text,
            "Günlük Hacim(Lot)": dom.xpath(xpath_query_initial)[6].text,
            "Günlük Hacim (TL)": dom.xpath(xpath_query_initial)[7].text,
            "Günlük Ortalama": dom.xpath(xpath_query_initial)[8].text,
            "Gün İçi En Düşük": dom.xpath(xpath_query_initial)[9].text,
            "Gün İçi En Yüksek": dom.xpath(xpath_query_initial)[10].text,
            "Açılış Fiyatı":dom.xpath(xpath_query_initial)[11].text,
            "Fiyat Adımı":dom.xpath(xpath_query_initial)[12].text,
            "Önceki Kapanış Fiyatı": dom.xpath(xpath_query_initial)[13].text,
            "Alt Marj Fiyatı": dom.xpath(xpath_query_initial)[14].text,
            "Üst Marj Fiyatı": dom.xpath(xpath_query_initial)[15].text,
            "20 Günlük Ortalama": dom.xpath(xpath_query_initial)[16].text,
            "52 Günlük Ortalama": dom.xpath(xpath_query_initial)[17].text,
            "Haftalık en Düşük": dom.xpath(xpath_query_initial)[18].text,
            "Haftalık en Yüksek": dom.xpath(xpath_query_initial)[19].text,
            "Yıllık en Düşük": dom.xpath(xpath_query_initial)[20].text,
            "Yıllık en Yüksek": dom.xpath(xpath_query_initial)[21].text,
            "Baz Fiyatı": dom.xpath(xpath_query_initial)[22].text

        }

    return data


def create_file(data):
    try:
        with open('companies_data.json', 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False)
        print('File created successfully!')
    except IOError as e:
        print("Couldn't open or write to file (%s)." % e)


def get_companies(n=None):
    data = []
    companies = []

    if n is None or n == 0:
        for company in table_body.find_all('a', href=True):
            companies_html_data.append(requests.get(company['href']).text)

        for company_html_data in companies_html_data:
            get_company_data(company_html_data)

        create_file(data)
    else:
        for i in range(n):
            companies.append(table_body.find_all('a', href=True)[i])

        for j in range(n):
            companies_html_data.append(requests.get(companies[j]['href']).text)
            data.append(get_company_data(companies_html_data[j]))

        create_file(data)


# get_companies(n: amount of company -> n:int)
get_companies(5)
