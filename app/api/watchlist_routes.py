from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import  db, Stock, Watchlist
from sqlalchemy.sql import text

watchlist_routes = Blueprint('watchlist', __name__)



@watchlist_routes.route('', methods=['POST'])
@login_required
def add_stock_to_watchlist():
    data = request.get_json()
    stock_id = data.get('stock_id')
    category = data.get('category', 'default')

    stock = Stock.query.get(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found."}), 404


    existing = db.session.execute(
        text("SELECT 1 FROM watchlist WHERE user_id=:user_id AND stock_id=:stock_id"),
        {"user_id": current_user.id, "stock_id": stock_id}
    ).fetchone()

    if existing:
        return jsonify({"error": "Stock already in watchlist."}), 409


    db.session.execute(
        text("""
            INSERT INTO watchlist (user_id, stock_id, category)
            VALUES (:user_id, :stock_id, :category)
        """),
        {"user_id": current_user.id, "stock_id": stock_id, "category": category}
    )
    db.session.commit()

    return jsonify({"message": "Stock added to watchlist with category."}), 201


@watchlist_routes.route('/', methods=['GET'])
@login_required
def view_watchlist():
    watchlist_items = Watchlist.query.filter_by(user_id=current_user.id).all()
    stocks_data = []
    for item in watchlist_items:

       stock = item.stock
       if stock:
            stocks_data.append({
                "id": item.id,
                "stock_id": stock.id,
                "symbol": stock.symbol,
                "name": stock.name,
                "price": stock.price,
                "category": stock.category
                # add additional categories
            })

    return jsonify(stocks_data), 200

# def update_category(user_id, stock_id, new_category):
#     sql = text("""
#         UPDATE watchlist SET category=:category
#         WHERE user_id=:user_id AND stock_id=:stock_id
#     """)
#     db.engine.execute(sql, category=new_category, user_id=user_id, stock_id=stock_id)


@watchlist_routes.route('/<int:watchlist_id>', methods=['PUT'])
@login_required
def update_watchlist_entry(watchlist_id):
    data = request.get_json()
    new_category = data.get('category')

    if not new_category:
        return jsonify({"error": "New category is required."}), 400

    watchlist_entry = Watchlist.query.filter_by(id=watchlist_id, user_id=current_user.id).first()
    if watchlist_entry:
        watchlist_entry.category = new_category
        db.session.commit()
        return jsonify(watchlist_entry.to_dict()), 200
    else:
        return jsonify({"error": "Watchlist entry not found."}), 404

@watchlist_routes.route('/<int:watchlist_id>', methods=['DELETE'])
@login_required
def remove_from_watchlist(watchlist_id):
    watchlist_entry = Watchlist.query.filter_by(id=watchlist_id, user_id=current_user.id).first()

    if not watchlist_entry:
        return jsonify({"error": "Watchlist entry not found."}), 404

    db.session.delete(watchlist_entry)
    db.session.commit()

    return '', 204
