import requests
from bs4 import BeautifulSoup
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def scrape_nifty_50():
    url = 'https://www.nseindia.com/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    nifty_50_table = soup.find('table', {'id': 'nifty-50-table'})
    rows = nifty_50_table.find_all('tr')[1:] 

    data = []
    for row in rows:
        columns = row.find_all('td')
        data.append({
            'symbol': columns[0].text.strip(),
            'price': columns[1].text.strip(),
            'change': columns[2].text.strip(),
            'percent_change': columns[3].text.strip(),
        })
    
   
    r.set('nifty_50_data', json.dumps(data))
