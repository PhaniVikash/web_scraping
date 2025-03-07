import ssl
import time
from os import getenv
import requests
import selectorlib
import smtplib
import sqlite3


connection = sqlite3.connect("data.db")


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
URL="http://programmer100.pythonanywhere.com/tours/"


def scrape(url):
   ''' Scrape the page source from the URL using requests.get function '''
   response = requests.get(url,headers=HEADERS)
   # convert it into a text using .text function , Then return the extracted text
   page_source= response.text
   return page_source


def extract(page_source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    # Use selectorlib Extractor class and store it in yaml file in source directory
    value = extractor.extract(page_source)["tours"]
    # Extract the required info and assign it to a variable
    return value

def send_email(message):
    # Send email function
    host = "smtp.gmail.com"
    port = 465

    username = "phanivikash@gmail.com"
    password = getenv("PASSWORD")
    receiver = "phanivikash@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host,port,context=context) as server :
        server.login(username,password)
        server.sendmail(username,receiver,message)
    print("Email was sent ")


def store(extracted):
    # data can be stored in txt doc or in SQL , we used SQL
    row = extracted.split(",")
    row = [i.strip() for i in row]
    # divide the text into list of items ,start a cursor to point the usage
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Events VALUES(?,?,?)",row)
    # Execute a SQL function and use commit to write the changes
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row=[i.strip() for i in row]
    band,city,date = row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Events WHERE band=? AND city = ? AND date = ? ",
                   (band,city,date))
    db_data=cursor.fetchall()
    print(db_data)
    return db_data


if __name__ == "__main__":
    while True:
        # Start a while loop to keep it running and use sleep function to control the loop time
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)


        if extracted != "No upcoming tours":
            # Read content data only if event is happening
            content = read(extracted)
            if not content:
                # Store and send email only if the event is fresh and not repeated
                store(extracted)
                send_email(message="Hey new event was found"+"\n"+extracted)
        time.sleep(2)



