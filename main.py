import requests
import selectorlib

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
URL="http://programmer100.pythonanywhere.com/tours/"

def scrape(url):
   ' Scrape the page source from the URL '
   response = requests.get(url,headers=HEADERS)
   page_source= response.text
   return page_source

def extract(page_source):
    selectorlib.Extractor.from_yaml_file("extract.yaml")


if __name__ == "__main__":
    print(scrape(URL))

