from polygon import RESTClient
import time
import requests
import datetime

def fetch_multiple_stocks_data(symbols, api_key):
    base_url = "https://api.polygon.io/v2/aggs/ticker"
    stock_data = []

    for symbol in symbols:

        url = f"{base_url}/{symbol}/prev?adjusted=true&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
                stock_info = {
                    'symbol': symbol,
                    'open': result.get('o'),
                    'close': result.get('c'),
                    'high': result.get('h'),
                    'low': result.get('l'),
                    'volume': result.get('v'),

                }
                stock_data.append(stock_info)
            else:
                stock_data.append({'symbol': symbol, 'error': 'No data found'})
        else:
            stock_data.append({'symbol': symbol, 'error': 'Failed to fetch data'})

    return stock_data



def fetch_stock_data_with_retry(symbol, api_key, retries=3, backoff_factor=0.3):
    for attempt in range(retries):
        try:
            return fetch_multiple_stocks_data(symbol, api_key)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                sleep_time = backoff_factor * (2 ** attempt)
                print(f"Rate limit exceeded. Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                raise e  # Re-raise the exception if it's not a 429 error
    return {'symbol': symbol, 'error': 'Max retries exceeded', 'success': False}
