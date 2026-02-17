import logging
import requests

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

def log_event(message, level="info"):
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)

def get_exchange_rates():
    url = "https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/ka/json"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()[0]['currencies']
            rates = {}
            for item in data:
                if item['code'] in ['USD', 'EUR', 'GBP']:
                    rates[item['code']] = item['rate']
            return rates
    except Exception as e:
        print(f"ვალუტის კურსის შეცდომა: {e}")

    return None