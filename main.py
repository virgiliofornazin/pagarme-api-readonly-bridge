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
    size = 200  # The number of items you want per page
    page = 1  # Start with the first page
    if filters:
        current_url = f"{initial_url}?page={page}&size={size}&navigation=True&{filters}"
    else:
        current_url = f"{initial_url}?page={page}&size={size}&navigation=True"
    # Get the first page to retrieve the total count
    response_data = get_data_from_page(current_url, head)
    try:
        total_items = response_data['paging']['total']
        total_pages = (total_items + size - 1) // size  # Calculate total number of pages
    # Now iterate through all pages and collect the data
    for page in range(1, total_pages + 1):
        if filters:
            current_url = f"{initial_url}?page={page}&size={size}&navigation=True&{filters}"
        else:
            current_url = f"{initial_url}?page={page}&size={size}&navigation=True"
        
        response_data = get_data_from_page(current_url, head)
        all_data.extend(response_data['data'])
    return all_data
 
#%%
app = FastAPI()

@app.get('/requerir/')
async def get_item(key: str,
                   chamada: str,
                   filters: Optional[str] = None):
    if key == 'f0d318283lmzanc81234asd234':
        initial_request_url = f"{BASE_URL}{chamada}"
        all_pages_data = get_all_pages_data(initial_url=initial_request_url, 
                                            head={"Authorization": f"Basic {os.environ.get('AUTH_HEADER')}"},
                                            filters=filters)
        return all_pages_data
    else: "Senha incorreta"
 
@app.get('/requerir_por_pagina/')
async def get_item(key: str,
                   chamada: str,
                   page: str,
                   size: str,
                   filters: Optional[str] = None):
    if key == 'f0d318283lmzanc81234asd234':
        if filters:
            current_url = f"{BASE_URL}{chamada}?page={page}&size={size}&navigation=True&{filters}"
        else:
            current_url = f"{BASE_URL}{chamada}?page={page}&size={size}&navigation=True"
        all_data = get_data_from_page(current_url, head={"Authorization": f"Basic {os.environ.get('AUTH_HEADER')}"})
        return all_data
    else: "Senha incorreta"

# %%
