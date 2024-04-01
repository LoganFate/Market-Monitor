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

    # Use ORM to check if the stock exists
    stock = Stock.query.get(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found."}), 404

    # Use ORM to check if the stock is already in the user's watchlist
    existing = Watchlist.query.filter_by(user_id=current_user.id, stock_id=stock_id).first()
    if existing:
        return jsonify({"error": "Stock already in watchlist."}), 409

    # Use ORM to add the stock to the watchlist
    new_watchlist_entry = Watchlist(user_id=current_user.id, stock_id=stock_id, category=category)
    db.session.add(new_watchlist_entry)
    try:
        db.session.commit()
        return jsonify({"message": "Stock added to watchlist successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add stock to watchlist.", "details": str(e)}), 500



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
