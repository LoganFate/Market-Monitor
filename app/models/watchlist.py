from .db import db, environment, SCHEMA, add_prefix_for_prod


class Watchlist(db.Model):
    __tablename__ = 'watchlist'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('stocks.id')), nullable=False)
    category = db.Column(db.String(50), nullable=True)

    user_watchlist = db.relationship('User', backref=db.backref('watchlist_stocks', lazy=True))
    stock = db.relationship('Stock', backref=db.backref('watchlisted_by_users', lazy=True))


    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'stock_id': self.stock_id,
            'category': self.category
        }
