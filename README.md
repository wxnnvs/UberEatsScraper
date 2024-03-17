# UberEatsScraper
Scrape a hell lot of  Uber Eats shops and their URL

## Installation (Manual)

1. Install [Python 3](https://www.python.org/downloads/)
2. Download the [latest release](github.com/wxnnvs/UberEatsScraper/releases/latest) to a dedicated folder
3. Install dependencies
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
4. Run `python3 main.py`

Results can be found under the `countries` folder

## Installation (Docker)

1. Install [Docker](https://www.docker.com/get-started/)
2. Run `docker run --rm -it -v .:/app/countries wxnnvs/ubereats-scraper` in a dedicated folder
3. The program will deploy automaticly

Results can be found in the folder you ran the container in
