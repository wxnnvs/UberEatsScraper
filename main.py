import requests
from bs4 import BeautifulSoup
from fp.fp import FreeProxy

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
#proxy = FreeProxy(rand=True, timeout=1).get()

countries = ["au", "be", "ca", "cl", "cr", "do", "ec", "sv", "fr", "de", "gt", "ie", "it", "jp", "ke", "mx", "nl", "nz", "pa", "pl", "pt", "za", "es", "lk", "se", "ch", "tw", "gb", "us"]
cities = ["antwerpen-anvers", "brussel-bruxelles-capitale", "gent-flandre-orientale", "li%C3%A8ge-li%C3%A8ge", "louvain-la-neuve-brabant-wallon", "namur-namur"]

for city in cities:
    if city == "li%C3%A8ge-li%C3%A8ge":
        print("Scraping LIÈGE...\n")
        with open("restaurants.txt", "a", encoding="utf-8") as file:
            file.write("\n\nLIÈGE\n")
            file.close()
    else:
        print(f"Scraping {city.upper()}...\n")
        with open("restaurants.txt", "a", encoding="utf-8") as file:
            file.write(f"\n\n{city.upper()}\n")
            file.close()
    url = f"https://www.ubereats.com/be/city/{city}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    shops = soup.find_all('a', {"data-test": "store-link"})

    for shop in shops:
        path = shop['href']
        page_link = "https://www.ubereats.com" + path
        names = shop.find_all('h3')
        for name in names:
            restaurant_name = name.text
            with open("restaurants.txt", "a", encoding="utf-8") as file:
                file.write(f"{restaurant_name}, {page_link}\n")
                file.close()