
import requests
from bs4 import BeautifulSoup
import csv

class  Parser:
    HEADERS = {
        'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'
        'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
    }

    HOST = "https://www.kivano.kg"

    def __init__(self,url,path) -> None:
        self.url = url
        self.path = path

    def get_html(self):
        request = requests.get(self.url,headers=self.HEADERS)
        return request.text

    def get_content(self,html):
        soup = BeautifulSoup(html,"html.parser")
        iteams = soup.find_all('div',class_='item product_listbox oh')
        new_list = []
        for iteam in iteams:
            new_list.append({
                "title": iteam.find("div",class_="listbox_title oh").find("a").get_text(strip=True),
                "price": iteam.find("div",class_="listbox_price text-center").get_text(strip= True)
            })
        return new_list

    def save_txt(self,iteams):
        with open(self.path,"w") as file:
            for iteam in iteams:
                file.write(f"Название:{iteam['title']}, цена:{iteam['price']}\n")

    def save(self, iteams):
        with open(self.path, 'w') as file:
            writer= csv.writer(file, delimiter=',')
            writer.writerow(['Названия','Цена' ])
            for iteam in iteams:
                writer.writerow([iteam['title'], iteam['price']])

parser = Parser(
    url='https://www.kivano.kg/{}'.format(input('name category:')),
    path='{}.csv'.format(input('name file:'))
)  

request = parser.get_html()
content = parser.get_content(request)
parser.save(content)