from app.models import db, Watchlist, environment, SCHEMA
from sqlalchemy.sql import text


def seed_watchlist():
    watchlist_items = [
        Watchlist(user_id=1, stock_id=1, category='Tech'),
        Watchlist(user_id=2, stock_id=2, category='Finance'),
        Watchlist(user_id=3, stock_id=3, category='Healthcare'),
        Watchlist(user_id=4, stock_id=4, category='Energy'),
        Watchlist(user_id=5, stock_id=5, category='Consumer Goods'),
    ]

    db.session.bulk_save_objects(watchlist_items)
    db.session.commit()

def undo_watchlist():
     if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.watchlist RESTART IDENTITY CASCADE;")
     else:
        db.session.execute(text("DELETE FROM watchlist"))
        db.session.commit()
