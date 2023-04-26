import csv
import requests
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.newportrentals.com"
URL = "https://www.newportrentals.com/jersey-city-apartment-buildings/roosevelt/"


def get_response():
    # create new request session
    sess = requests.Session()
    sess.get(URL)
    # et payload data for requests server in browser (developer tools page)
    payload_data = {"buildingid": "ngofmfgp"}
    data_url = "https://www.newportrentals.com/ajax/getbuildingunits.asp"
    # post request a server 
    res = sess.post(data_url, data=payload_data, timeout=10)
    return res


def extract_data(res):
    soup = bs(res.text, 'lxml')
    # extract the information we want using beautifulSoup
    data_dict = {
        "address": soup.find('h3', {'class': 'body-text text-medium feat-unit-info-text'}).text,
        "street": soup.find('div', {'class': 'body-text text-light feat-unit-info-text feat-unit-info-text--space-above'}).text,
        "bedroom": soup.find('div', {'class': 'unit-stats-item'}).text.split()[0],
        "bathroom": soup.findAll('div', {'class': 'unit-stats-item'})[1].text.strip(),
        "sq": soup.findAll('div', {'class': 'unit-stats-item'})[2].text.split()[0],
        "price": soup.select('body > div > div > div.feat-unit-info.text-center > div.feat-apt-price.body-text.text-light.text-white')[0].text,
        "url": f"{BASE_URL}{soup.find('div', {'class': 'carousel-slide carousel-slide--feat-unit'}).get('href')}",
    }
    return data_dict


def save_csv(data_dict):
    # save in csv file and use the dict key as column names
    with open("csv/data.csv", 'w') as f:
        w = csv.DictWriter(f, data_dict.keys())
        w.writeheader()
        w.writerow(data_dict)

    
def main():
    # ctrl function
    res = get_response()
    data_dict = extract_data(res)
    save_csv(data_dict)

main()