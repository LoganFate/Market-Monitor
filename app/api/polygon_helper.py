from polygon import RESTClient
import time
import requests

def fetch_stock_data(symbol, api_key):
    try:
        client = RESTClient(api_key)

        # Fetch the last close price, last trade, and last quote
        # Assuming the API provides a way to fetch the previous close directly, otherwise, we use aggregates

        # Fetch daily aggregates (OHLC) for the previous trading day
        # You might need to adjust the 'from_' and 'to' dates to ensure you're fetching the correct previous trading day
        prev_day_ohlc = client.get_aggs(symbol, 1, "day", "2023-01-01", "2023-01-02")  # Example dates, adjust accordingly

        # Fetch the last trade
        last_trade = client.get_last_trade(symbol)

        # Fetch the last quote
        last_quote = client.get_last_quote(symbol)

        # Construct the result dictionary with the required information
        result = {
            'symbol': symbol,
            'previous_close': prev_day_ohlc[0].close if prev_day_ohlc else None,  # Adjust according to actual response structure
            'last_trade_price': last_trade.price if last_trade else None,
            'last_ask_price': last_quote.ask_price if last_quote else None,  # Adjust field name according to actual response
            'success': True
        }
    except Exception as e:
        result = {
            'symbol': symbol,
            'error': str(e),
            'success': False
        }
    finally:
        # Clean up the client resource


        return result

    import time
import requests

def fetch_stock_data_with_retry(symbol, api_key, retries=3, backoff_factor=0.3):
    for attempt in range(retries):
        try:
            return fetch_stock_data(symbol, api_key)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                sleep_time = backoff_factor * (2 ** attempt)
                print(f"Rate limit exceeded. Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                raise e  # Re-raise the exception if it's not a 429 error
    return {'symbol': symbol, 'error': 'Max retries exceeded', 'success': False}
