import requests
import time
from datetime import datetime


# API to get crypto-currencies prices and info
BITCOIN_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# IFTTT custom event which I created
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{}'
# My key to access my custom IFTTT event
IFTTT_KEY = 'jjhc1h0PM7xe1CCQD5odojJs0LASBFUGCd58winr_9F'


def get_latest_bitcoin_price():
    """
    A function to get latest bitcoin price by sending to BITCOIN_API_URL a request which has 
    my account key.
    API respond with a JSON cointains all crypto-currencies info and prices.

    input   :   Void
    output  :   latest bitcoin prices (int)
    """

    session = requests.Session()
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '768bf427-8541-4c43-8f9c-871a422057b4',
    }
    session.headers.update(headers)

    response = session.get(BITCOIN_API_URL)
    return int(response.json()['data'][0]['quote']['USD']['price'])


def post_ifttt_webhook(event, value):
    """
    A function to trigger my IFTTT custom event -IFTTT_WEBHOOKS_URL-.
    attaching a JSON contain a value.
    this API sends an email telling the latest bitcoin price and pushing a mobile notification.

    inputs  :   event (str)   -   value (any type)
                
                event   :  values (bitcoin_price_emergency , bitcoin_price_update).
                value   :  expected to be the latest bitcoin price.
    output  :   Void
    """

    data = {'value1': value}
    event_url = IFTTT_WEBHOOKS_URL.format(event, IFTTT_KEY)

    requests.post(event_url, json=data)


# a threshold when bitcoin price reachs, sends an emergency alert
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