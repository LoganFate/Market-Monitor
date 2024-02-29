from .db import db, environment, SCHEMA

class Stock(db.Model):
    __tablename__ = 'stocks'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    market_cap = db.Column(db.Float, nullable=False)
    pe_ratio = db.Column(db.Float, nullable=False)
    sector = db.Column(db.String(50), nullable=False)
    previous_close = db.Column(db.Float)  # Add this field
    # Add other fields as needed

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'market_cap': self.market_cap,
            'pe_ratio': self.pe_ratio,
            'sector': self.sector,
            'previous_close': self.previous_close,
            # Add other fields as needed
        }
