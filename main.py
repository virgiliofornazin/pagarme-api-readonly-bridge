#%%
import requests
from fastapi import FastAPI
from typing import Optional
import os
# from dotenv import load_dotenv
# load_dotenv()

BASE_URL = "https://api.pagar.me/core/v5/"

def get_data_from_page(url, head):
    response = requests.get(url, headers=head)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def get_all_pages_data(initial_url, head, filters=None):
    all_data = []
    if filters:
        current_url = f"{initial_url}?page=1&size=200&navigation=True&{filters}"
    else: current_url = f"{initial_url}?page=1&size=200&navigation=True"
 
    next_page_url = initial_url  # Initialize next_page_url with the initial_url
   
    while next_page_url:
        response_data = get_data_from_page(current_url, head)
        all_data.extend(response_data['data'])  # Assuming each page has a 'data' key with the required data

        next_page_url = response_data.get('paging', {}).get('next')
        
        # If there are date filters, update the current_url with them
        if filters:
            current_url = f"{next_page_url}&{filters}"
        else:
            current_url = next_page_url
    

    return all_data

#%%
app = FastAPI()

@app.get('/requerir/')
async def get_item(key: str, chamada: str,
                   filters: Optional[str] = None):
    if key == "f0d318283lmzanc81234asd234":
        initial_request_url = f"{BASE_URL}{chamada}"
	all_pages_data = get_all_pages_data(initial_url=initial_request_url, 
                                        head={"Authorization": f"Basic {os.environ.get('AUTH_HEADER')}"},
                                        filters=filters)

        return all_pages_data
    else:
	return "access denied"

# %%

