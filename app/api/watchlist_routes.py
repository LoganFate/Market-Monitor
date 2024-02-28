from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import  db, User, Stock
from sqlalchemy.sql import text

watchlist_routes = Blueprint('watchlist', __name__)



@watchlist_routes.route('/watchlist', methods=['POST'])
@login_required
def add_stock_to_watchlist():
    data = request.get_json()
    stock_id = data.get('stock_id')

    if not stock_id:
        return jsonify({"error": "Stock ID is required."}), 400

    stock = Stock.query.get(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found."}), 404

    if stock in current_user.stocks:
        return jsonify({"error": "Stock already in watchlist."}), 409

    current_user.stocks.append(stock)
    db.session.commit()

    return jsonify({"message": "Stock added to watchlist successfully."}), 201


@watchlist_routes.route('/watchlist', methods=['GET'])
@login_required
def view_watchlist():
    stocks_data = [{
        "id": stock.id,
        "symbol": stock.symbol,
        "name": stock.name,
        "price": stock.price
        # Add other fields later if required
    } for stock in current_user.stocks]

    return jsonify(stocks_data), 200

def update_category(user_id, stock_id, new_category):
    sql = text("""
        UPDATE user_watchlist SET category=:category
        WHERE user_id=:user_id AND stock_id=:stock_id
    """)
    db.engine.execute(sql, category=new_category, user_id=user_id, stock_id=stock_id)


@watchlist_routes.route('/watchlist/', methods=['PUT'])
@login_required
def update_watchlist_category():
    data = request.get_json()
    stock_ids = data.get('stock_ids')
    new_category = data.get('new_category')


    if not stock_ids or not new_category:
        return jsonify({"error": "Missing stock IDs or category"}), 400


    for stock_id in stock_ids:
        update_category(current_user.id, stock_id, new_category)

    db.session.commit()

    return jsonify({"message": "Categories updated successfully."}), 200

@watchlist_routes.route('/watchlist', methods=['DELETE'])
@login_required
def remove_from_watchlist():
    stock_id = request.args.get('stock_id')

    if not stock_id:
        return jsonify({"error": "Stock ID is required."}), 400

    stock = Stock.query.filter_by(id=stock_id).first()
    if not stock or stock not in current_user.stocks:
        return jsonify({"error": "Stock not found in watchlist."}), 404

    current_user.stocks.remove(stock)
    db.session.commit()

    return '', 204
