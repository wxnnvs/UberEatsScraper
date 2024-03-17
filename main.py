import requests
from bs4 import BeautifulSoup
import json
import os
import signal
import argparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

countries = ["au", "be", "ca", "cl", "cr", "do", "ec", "sv", "fr", "de", "gt", "ie", "jp", "ke", "mx", "nl", "nz", "pa", "pl", "pt", "za", "es", "lk", "se", "ch", "tw", "gb"]

parser = argparse.ArgumentParser(description="Scrape data for a specific country.")
parser.add_argument("--country", type=str, help="The country to scrape data for.")
args = parser.parse_args()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def end(signal, frame):
    print("Exiting...")
    with open(f"countries/{c}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, end)

# the actual stuff
clear()
if args.country == None:
    print("Scraping all countries...")
    for c in countries:
        country = requests.get(f"https://restcountries.com/v3.1/alpha/{c}?fields=name", headers=headers, timeout=10).json()["name"]["common"]
        # Check if the 'countries' folder exists, create it if it doesn't
        if not os.path.exists('countries'):
            os.makedirs('countries')
        
        data = {
            "country": country.upper(),
            "cities": []
        }

        print(f"Scraping {country}...")

        url = f"https://www.ubereats.com/{c}/location"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            exit(1)

        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.find_all('a')
        for link in links:
            href = link.get('href')  # Get href attribute if it exists
            name = link.get_text().strip()
            if href and href.startswith(f"/{c}/city"):
                city_url = f"https://www.ubereats.com{href}"
                city_data = {
                    "city": name,
                    "shops": []
                }

                city_response = requests.get(city_url, headers=headers, timeout=10)
                city_soup = BeautifulSoup(city_response.content, "html.parser")
                shops = city_soup.find_all('a', {"data-test": "store-link"})
                for shop in shops:
                    path = shop.get('href')
                    page_link = "https://www.ubereats.com" + path
                    names = shop.find_all('h3')
                    for name in names:
                        restaurant_name = name.get_text().strip()
                        shop_data = {
                            "name": restaurant_name,
                            "link": page_link
                        }
                        city_data["shops"].append(shop_data)

                data["cities"].append(city_data)

        end()
elif args.country in countries:
    c = args.country
    country = requests.get(f"https://restcountries.com/v3.1/alpha/{c}?fields=name", headers=headers, timeout=10).json()["name"]["common"]
    # Check if the 'countries' folder exists, create it if it doesn't
    if not os.path.exists('countries'):
        os.makedirs('countries')
    
    data = {
        "country": country.upper(),
        "cities": []
    }

    print(f"Scraping {country}...")

    url = f"https://www.ubereats.com/{c}/location"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all('a')
    for link in links:
        href = link.get('href')  # Get href attribute if it exists
        name = link.get_text().strip()
        if href and href.startswith(f"/{c}/city"):
            city_url = f"https://www.ubereats.com{href}"
            city_data = {
                "city": name,
                "shops": []
            }

            city_response = requests.get(city_url, headers=headers, timeout=10)
            city_soup = BeautifulSoup(city_response.content, "html.parser")
            shops = city_soup.find_all('a', {"data-test": "store-link"})
            for shop in shops:
                path = shop.get('href')
                page_link = "https://www.ubereats.com" + path
                names = shop.find_all('h3')
                for name in names:
                    restaurant_name = name.get_text().strip()
                    shop_data = {
                        "name": restaurant_name,
                        "link": page_link
                    }
                    city_data["shops"].append(shop_data)

            data["cities"].append(city_data)

    end()
