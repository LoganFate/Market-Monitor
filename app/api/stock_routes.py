from flask import Blueprint, jsonify
from app.models import  db, Stock

stock_routes = Blueprint('stocks', __name__)

@stock_routes.route('/api/stocks', methods=['GET'])
def get_stocks():
    """
    User will be able to view stocks on the site.
    """
    stocks = Stock.query.all()
    return jsonify([stock.to_dict() for stock in stocks]), 200
