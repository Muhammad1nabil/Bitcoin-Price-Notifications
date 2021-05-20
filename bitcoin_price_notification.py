import requests
import time
from datetime import datetime

from requests.api import post


BITCOIN_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{}'
IFTTT_KEY = 'jjhc1h0PM7xe1CCQD5odojJs0LASBFUGCd58winr_9F'


def get_latest_bitcoin_price():
    session = requests.Session()
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '768bf427-8541-4c43-8f9c-871a422057b4',
    }
    session.headers.update(headers)

    response = session.get(BITCOIN_API_URL)
    return int(response.json()['data'][0]['quote']['USD']['price'])


def post_ifttt_webhook(event, value):
    data = {'value1': value}
    event_url = IFTTT_WEBHOOKS_URL.format(event, IFTTT_KEY)

    requests.post(event_url, json=data)


BITCOIN_PRICE_THRESHOLD = 100000

def main():
    price = get_latest_bitcoin_price()
    date = datetime.today().date()
    print("{}\t=>\t{}".format(date, price))

    if price >= BITCOIN_PRICE_THRESHOLD:
        post_ifttt_webhook('bitcoin_price_emergency', price)
    else:
        post_ifttt_webhook('bitcoin_price_update', price)

if __name__ == '__main__':
    main()