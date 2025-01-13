import pandas as pd
import requests
import os
import hmac
import time
import json
import hashlib
import base64
import logging, logging.config
from dotenv import load_dotenv
from constants import BROKERAGE

logging.basicConfig(
    filename="trade_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Firi(): 

    load_dotenv()
    _api_url="https://api.firi.com/"

    def __init__(self) -> None:
        self._api_key = os.getenv("API_KEY")
        self._secret_key = os.getenv("SECRET_KEY")
        self._client_id = os.getenv("CLIENT_ID")


        if not all([self._api_key, self._secret_key, self._client_id]):
            raise ValueError("API_KEY, SECRET_KEY, and CLIENT_ID must be set.")

    def create_hmac(data: str, key:str):
        """
    Create an HMAC signature using HmacSHA256.
    Args:
        data (str): The message to sign.
        key (str): The secret key.
    Returns:
        str: Hexadecimal HMAC signature.
        """
        key_bytes = key.encode("utf-8")
        data_bytes = data.encode("utf-8")

        hmac_instance = hmac.new(key_bytes, data_bytes, hashlib.sha256)
        return hmac_instance.hexdigest()


    def signature(self, endpoint):
        """Generate HMAC authentication header."""
        timestamp = int(time.time())
        validity_period = 2000

        message = json.dumps({"timestamp":timestamp, "validity":validity_period})
        signature = self.create_hmac(message, self._secret_key)
        return signature


    def template_func(self, endpoint, authenticated=False):
        """Generic method to make API requests."""
        url = self._api_url+endpoint
        headers = {"Authorization":f"Bearer {self._api_key}"}

        try: 
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                logging.error(f"Invaid JSON repsonse from {url}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for {url}: {e}")
            return None

    def get_time(self):
        """Fetch the server time (unauthenticated)."""
        logging.info("Fetching server time...")
        data = self.template_func("time")
        if data:
            logging.info(f"Server time: {data}")
        return data
    
    def get_transactions(self):
        return self.template_func("v2/history/transactions")
    
    def get_transactions_by_data(self, month, year):
        return self.template_func(f"v2/history/transactions/{month}/{year}")
    
    def meth(self):
        print(self._api_key)
        print(self._client_id)
        print(self._secret_key)


if __name__ == "__main__":
    firi = Firi()
    firi.get_time()
  
