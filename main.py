import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
API_KEY = os.environ.get("API_KEY")

# Replace these with the actual API URLs
USD_PRICE_API = f"http://api.navasan.tech/latest/?api_key={API_KEY}&item=usd_sell"
DIRHAM_PRICE_API = f"http://api.navasan.tech/latest/?api_key={API_KEY}&item=dirham_dubai"




def get_usd_price():
    response = requests.get(USD_PRICE_API)
    data = response.json()
    return float(data["usd_sell"]["value"])


def get_dirham_price():
    response = requests.get(DIRHAM_PRICE_API)
    data = response.json()
    return float(data["dirham_dubai"]["value"])


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)


def main():
    usd_price = get_usd_price()
    dirham_price = get_dirham_price()
    calculated_usd_price = dirham_price * 3.67

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if calculated_usd_price < usd_price:
        message = (f"[{current_time}] The calculated USD price ({calculated_usd_price}) is lower than the fetched USD "
                   f"price ({usd_price}).")
        send_telegram_message(message)
    else:
        message = (f"[{current_time}] The calculated USD price ({calculated_usd_price}) is higher than or equal to the "
                   f"fetched USD price ({usd_price}).")
        send_telegram_message(message)


if __name__ == "__main__":
    main()
