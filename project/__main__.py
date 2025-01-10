import pandas as pd
import os, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
print(API_KEY)

class Firi(): 
    api_url = "https://api.firi.com/"
    
    @classmethod
    def template_func(cls, resource):
        try: 
            response = requests.get(cls.api_url+resource)

            if response.status_code == 200:
                data = response.json()
                print("API Repsonse: ", data)
            else:
                print(f"Error: status code {response.status_code}")
                print("Response text:", response.text)

        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)

    def get_time(cls):
        return cls.template_func("time")

    def get_transactions(cls):
        return cls.template_func("v2/history/transactions")
    
    def get_transactions_by_data(cls, month, year):
        return cls.template_func(f"v2/history/transactions/{month}/{year}")

    

firi = Firi()
firi.get_time()
firi.get_transactions()

