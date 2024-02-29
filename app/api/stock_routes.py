from flask import Blueprint, jsonify
from app.models import db, Stock
from .polygon_helper import fetch_stock_data
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
        symbol = stock.symbol
        live_data_response = fetch_stock_data(symbol, API_KEY)

        if live_data_response.get('success'):
            # Update stock data with live data
            stock.previous_close = live_data_response.get('previous_close')
            # Add other fields as needed

            # Commit changes to the database
            db.session.commit()

            # Append enriched stock data to the response
            enriched_stock_data = {
                'symbol': symbol,
                'name': stock.name,
                'price': stock.price,
                'category': stock.category,
                'market_cap': stock.market_cap,
                'pe_ratio': stock.pe_ratio,
                'sector': stock.sector,
                'previous_close': stock.previous_close,
                # Add other fields as needed
            }
            enriched_stocks.append(enriched_stock_data)
        else:
            print(f"Error fetching live data for {symbol}: {live_data_response.get('error', 'Unknown error')}")

    return jsonify(enriched_stocks), 200
