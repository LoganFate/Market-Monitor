from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import  db, Stock, Watchlist
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
    stocks_data = []
    for watchlist_entry in current_user.watchlist_stocks:

        if watchlist_entry.stock:
            stocks_data.append({
                "id": watchlist_entry.id,
                "stock_id": watchlist_entry.stock.id,
                "symbol": watchlist_entry.stock.symbol,
                "name": watchlist_entry.stock.name,
                "price": watchlist_entry.stock.price,
                "category": watchlist_entry.stock.category
                # add additional categories
            })
        else:
            print(f"Watchlist entry {watchlist_entry.id} has no associated stock.")

    return jsonify(stocks_data), 200

def update_category(user_id, stock_id, new_category):
    sql = text("""
        UPDATE watchlist SET category=:category
        WHERE user_id=:user_id AND stock_id=:stock_id
    """)
    db.engine.execute(sql, category=new_category, user_id=user_id, stock_id=stock_id)


@watchlist_routes.route('/', methods=['PUT'])
@login_required
def update_watchlist_by_stock():
    data = request.get_json()
    stock_id = data.get('stock_id')
    new_category = data.get('category')


    if not stock_id or not new_category:
        return jsonify({"error": "Missing stock ID or new category"}), 400


    updated_entries = Watchlist.query.filter_by(user_id=current_user.id, stock_id=stock_id).update({'category': new_category})


    if updated_entries == 0:
        return jsonify({"error": "No watchlist items found for the provided stock ID"}), 404


    try:
        db.session.commit()
        return jsonify({"message": "Watchlist updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update watchlist item(s). Error: {str(e)}"}), 500

@watchlist_routes.route('/', methods=['DELETE'])
@login_required
def remove_from_watchlist():
    data = request.get_json()
    stock_id = data.get('stock_id')

    if not stock_id:
        return jsonify({"error": "Stock ID is required."}), 400

    watchlist_entry = Watchlist.query.filter_by(user_id=current_user.id, stock_id=stock_id).first()

    if not watchlist_entry:
        return jsonify({"error": "Stock not found in watchlist."}), 404

    db.session.delete(watchlist_entry)
    db.session.commit()

    return '', 204
