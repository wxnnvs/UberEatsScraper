import requests
from bs4 import BeautifulSoup
from fp.fp import FreeProxy
import json

url = "https://www.ubereats.com/be/category/gent-flandre-orientale/fast-food"

#proxy = FreeProxy(rand=True, timeout=1).get()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status() 
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)
    exit(1)

soup = BeautifulSoup(response.content, "html.parser")

shops = soup.find_all('div', class_=["ak", "bl"])

for shop in shops:
    names = shop.find_all('h3', class_=["ko", "ct", "ae", "ag"])
    links = shop.find_all('a')
    for name, link in zip(names, links):
        restaurant_name = name.text
        page_link = "https://www.ubereats.com" + link['href']
        print(restaurant_name, page_link)

        try:
            response = requests.get(page_link, headers=headers, timeout=10)
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            exit(1)

        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all('div', class_=["kh", "ki", "pm", "bl"])
        for product in products:
            names = soup.find_all('span')
            for name in names:
                print(name.text)
