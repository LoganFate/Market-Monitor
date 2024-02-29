from polygon import RESTClient

def fetch_previous_close(symbol, api_key):
    try:
        client = RESTClient(api_key)
        response = client.stocks_equities_previous_close(symbol)
        if response and response.results:
            result = {
                'symbol': symbol,
                'previous_close': response.results[0].c,
                'success': True
            }
        else:
            result = {'symbol': symbol, 'error': 'No data found', 'success': False}
    except Exception as e:
        result = {'symbol': symbol, 'error': str(e), 'success': False}
    finally:
        client.close()  # Ensure the client is closed properly

    return result
