from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import  db, User, Stock
from sqlalchemy.sql import text

watchlist_routes = Blueprint('watchlist', __name__)



@watchlist_routes.route('/', methods=['POST'])
@login_required
def add_stock_to_watchlist():
    data = request.get_json()
    stock_id = data.get('stock_id')
    category = data.get('category', 'default')

    stock = Stock.query.get(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found."}), 404


    existing = db.session.execute(
        text("SELECT 1 FROM user_watchlist WHERE user_id=:user_id AND stock_id=:stock_id"),
        {"user_id": current_user.id, "stock_id": stock_id}
    ).fetchone()

    if existing:
        return jsonify({"error": "Stock already in watchlist."}), 409


    db.session.execute(
        text("""
            INSERT INTO user_watchlist (user_id, stock_id, category)
            VALUES (:user_id, :stock_id, :category)
        """),
        {"user_id": current_user.id, "stock_id": stock_id, "category": category}
    )
    db.session.commit()

    return jsonify({"message": "Stock added to watchlist with category."}), 201


@watchlist_routes.route('/', methods=['GET'])
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


@watchlist_routes.route('/<int:watchlistId>', methods=['PUT'])
@login_required
def update_watchlist_category():
    data = request.get_json()
    stock_ids = data.get('stock_ids')
    new_category = data.get('new_category')

    if not stock_ids or not new_category:
        return jsonify({"error": "Missing stock IDs or category"}), 400


    for stock_id in stock_ids:
        sql = text("""
            UPDATE user_watchlist
            SET category = :new_category
            WHERE user_id = :user_id AND stock_id = :stock_id
        """)
        db.engine.execute(sql, new_category=new_category, user_id=current_user.id, stock_id=stock_id)

    db.session.commit()

    return jsonify({"message": "Categories updated successfully."}), 200

@watchlist_routes.route('/<int:watchlistId>', methods=['DELETE'])
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
