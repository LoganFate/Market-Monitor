from flask import Blueprint, jsonify
from app.models import db, Stock
from .polygon_helper import fetch_multiple_stocks_data
import os

stock_routes = Blueprint('stocks', __name__)

API_KEY = os.getenv('POLYGON_API_KEY')

@stock_routes.route('/', methods=['GET'])
def get_stocks():
    if not API_KEY:
        print("API_KEY is not set. Please check your environment variables.")
        return jsonify({'error': 'API_KEY is missing'}), 500

    # Fetch symbols from the database
    stocks = Stock.query.all()
    symbols = [stock.symbol for stock in stocks]

    # Fetch live data for all symbols at once
    live_data_responses = fetch_multiple_stocks_data(symbols, API_KEY)

    enriched_stocks = []
    for response in live_data_responses:
        if 'error' not in response:
            stock = next((s for s in stocks if s.symbol == response['symbol']), None)
            if stock:
                # Update database object if necessary (optional)
                # stock.price = response['close']
                # db.session.commit()

                enriched_stock_data = {
                    'symbol': response['symbol'],
                    'name': stock.name,
                    'live_open': response.get('open'),
                    'live_close': response.get('close'),
                    'live_high': response.get('high'),
                    'live_low': response.get('low'),
                    'live_volume': response.get('volume'),
                    # Map other fields as needed
                }
                enriched_stocks.append(enriched_stock_data)
        else:
            print(f"Error fetching live data for {response['symbol']}: {response['error']}")

    return jsonify(enriched_stocks), 200
