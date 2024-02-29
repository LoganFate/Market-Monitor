from flask import Blueprint, jsonify
from app.models import db, Stock
from .polygon_helper import fetch_previous_close  # Make sure this import path is correct
import os

stock_routes = Blueprint('stocks', __name__)

API_KEY = os.getenv('POLYGON_API_KEY')

@stock_routes.route('/', methods=['GET'])
def get_stocks():
    """
    Fetch stocks from the database and enrich them with live data from Polygon.io.
    """
    if not API_KEY:
        print("API_KEY is not set. Please check your environment variables.")
        return jsonify({'error': 'API_KEY is missing'}), 500

    stocks = Stock.query.all()
    enriched_stocks = []

    for stock in stocks:
        symbol = stock.symbol  # Assuming your Stock model has a 'symbol' attribute
        live_data_response = fetch_previous_close(symbol, API_KEY)  # Pass the API key as an argument

        print(f"Fetching live data for {symbol}: {live_data_response}")  # Debugging line

        if live_data_response.get('success'):
            stock_data = stock.to_dict()
            # Enriching the stock data with live data from Polygon
            stock_data['previous_close'] = live_data_response.get('previous_close')
            enriched_stocks.append(stock_data)
        else:
            print(f"Error or no data for {symbol}: {live_data_response.get('error', 'Unknown error')}")
            enriched_stocks.append(stock.to_dict())

    return jsonify(enriched_stocks), 200
