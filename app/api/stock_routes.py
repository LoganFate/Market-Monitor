from flask import Blueprint, jsonify
import requests
from app.models import  db, Stock

stock_routes = Blueprint('stocks', __name__)

@stock_routes.route('/api/stocks', methods=['GET'])
def get_stocks():
    """
    User will be able to view stocks on the site, enriched with live data from the Polygon API.
    """
    # Example: Fetching all stocks from your database
    stocks = Stock.query.all()

    # Prepare a list to hold enriched stock data
    enriched_stocks = []

    for stock in stocks:
        # For each stock, attempt to fetch additional data from the Polygon API
        symbol = stock.symbol  # Assuming each stock model has a 'symbol' field
        url = f'https://api.polygon.io/v1/open-close/{symbol}/2023-02-28?apiKey={API_KEY}'  # Example API call
        response = requests.get(url)

        if response.status_code == 200:
            polygon_data = response.json()
            # Add or update information from Polygon to your stock data
            # This is just an example; adjust according to your data model and needs
            stock_dict = stock.to_dict()
            stock_dict['polygon_data'] = polygon_data
            enriched_stocks.append(stock_dict)
        else:
            # Handle cases where the Polygon API does not return data
            enriched_stocks.append(stock.to_dict())

    return jsonify(enriched_stocks), 200
