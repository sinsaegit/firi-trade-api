import pandas as pd
import requests
import os
import hmac
import time
import json
import hashlib
import logging, logging.config
from dotenv import load_dotenv
from requests.exceptions import RequestException
from constants import BROKERAGE

script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "api_access.log")

logging.basicConfig(
    filename=log_file_path,
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

    def create_hmac(self, data: str, key:str) -> str:
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


    def create_signature(self, endpoint: str, validity: int = 2000, extra_data: dict = None) -> dict:
        """Generate HMAC authentication header."""
        timestamp = int(time.time())

        msg_body = {"timestamp":timestamp,"validity":validity}
        if extra_data:
            msg_body.update(extra_data)

        signature = self.create_hmac(json.dumps(msg_body).strip(), self._secret_key)
        

        return {
            "firi-access-key":self._api_key,
            "firi-user-signature":signature,
            "firi-user-clientid":self._client_id
        }, {"timestamp":str(timestamp),"validity":str(validity)}


    def template_func(self, endpoint: str, authenticated: bool = False, method: str = "GET", data: dict = None) -> dict:
        """Generic method to make API requests."""
        url = self._api_url+endpoint
        # print(url)
        headers = {}
        query_params = {}

        if authenticated:
            headers, query_params = self.create_signature(endpoint, extra_data=data)
        
        if query_params:
            query_string = "".join(f"&{key}={value}" for key, value in query_params.items())
            # url += f"&{query_string}" if "?" in url else f"?{query_string}"


        logging.info(f"Request URL: {url}")
        logging.info(f"Client ID: {self._client_id}")
        logging.info(f"Request headers: {query_params}")
        if data:
            logging.info(f"Additional request data: {data}")

        try:
            if method == "GET":
                response = requests.get(url=url, headers=headers)
            elif method == "POST":
                response = requests.post(url=url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            logging.info(f"Response Status Code: {response.status_code}")
            logging.info(f"Response JSON: {response.text}")
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for {url}: {e}")
            return {"error": "API request failed"}


    def get_time(self) -> dict:
        """Fetch the server time (unauthenticated)."""
        logging.info("Fetching server time...")
        return self.template_func("time", authenticated=False)
    
    def get_transactions(self, direction: str = "end", count: int = 10) -> dict:
        """
        Fetch transaction history (authenticated).
        Args:
            direction (str): "start" or "end" to specify direction of transaction history.
            count (int): Number of transactions to fetch.
        Returns:
            dict: Transaction history.
        """
        logging.info("Fetching transaction history...")
        endpoint = f"v2/history/transactions?direction={direction}&count={count}"
        response = self.template_func(endpoint=endpoint, authenticated=True)

        if response is None:
            logging.error("Failed to fetch transactions. Response is None")
            return {"error": "Failed to fetch transactions. Check logs for details."}
        return response 
    
    def get_transactions_by_year(self, year: int, direction: str = "end") -> dict:
        """
        Fetch transaction history for a specific year (authenticated).
        Args:
            year (int): The year to fetch transactions for (must be > 2017).
            direction (str): "start" or "end" to specify direction of transaction history.
        Returns:
            dict: Transaction history or an error message.
        """
        if year <= 2017:
            raise ValueError("Year must be greater than 2017.")
        
        logging.info("Fetching transaction history for {year}")
        endpoint = f"v2/history/transactions/{year}?direction={direction}"
        response = self.template_func(endpoint=endpoint, authenticated=True)

        if response is None:
            logging.error(f"Failed to fetch transactions for year {year}. Response is None.")
            return {"error": f"Failed to fetch transactions for year {year}. Check logs for details."}
        return response
    
    def get_transactions_by_year_month(self, month: int, year: int, direction: str = "end") -> dict: 
        if year <= 2017:
            raise ValueError("Year must be greater than 2017.")
        if (month < 1 or month > 12):
            raise ValueError("Month must be between 1 and 12") 
        
        logging.info(f"Fetching transaction history for year {year}, month {month}...")
        endpoint = f"v2/history/transactions/{month}/{year}?direction={direction}"
        response = self.template_func(endpoint=endpoint, authenticated=True, method="GET")

        if response is None:
            logging.error(f"Failed to fetch transactions for year {year}, month {month}. Response is None.")
            return {"error": f"Failed to fetch transactions for year {year}, month {month}. Check logs for details."}
        return response
    
    def get_orders(self, count: int, order_type: str = None):
        """
        Fetch history of all orders (authenticated).
        Args:
            order_type (str): The type of orders to fetch (e.g., "buy", "sell").
            count (int): The number of orders to fetch.
        Returns:
            dict: Order history or an error message.
        NOTE: query param type is optional and is deprecated.
        """
        logging.info(f"Fetching order history with type={order_type} and count={count}...")
        endpoint = f"v2/history/orders?"

        query_params = []
        if order_type:
            query_params.append(f"type={order_type}")
        query_params.append(f"count={count}")

       

        endpoint += "&".join(query_params)
        response = self.template_func(endpoint=endpoint, authenticated=True, method="GET")

        if response is None:
            logging.error("Failed to fetch order history. Response is None.")
            return {"error": "Failed to fetch order history. Check logs for details."}
        return response


  
if __name__ == "__main__":
    firi = Firi()
    print(firi.get_time())  

    # transactions = firi.get_transactions_by_year(year=2021,direction="end")
    # transactions = firi.get_transactions_by_year_month(month= 12, year=2021, direction="end")
    orders = firi.get_orders(10)
    

    for i in orders:
        print(i,"\n")
