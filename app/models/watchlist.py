from .db import db, environment, SCHEMA, add_prefix_for_prod

watchlist_stocks = db.Table('watchlist_stocks',
    db.Column('watchlist_id', db.Integer, db.ForeignKey('watchlist.id'), primary_key=True),
    db.Column('stock_id', db.Integer, db.ForeignKey('stock.id'), primary_key=True)
)

class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Define the relationship using the association table
    stocks = db.relationship('Stock', secondary=watchlist_stocks, lazy='subquery',
                             backref=db.backref('watchlists', lazy=True))
