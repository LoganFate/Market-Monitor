from .db import db, environment, SCHEMA

class Stock(db.Model):
    __tablename__ = 'stocks'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    market_cap = db.Column(db.BigInteger, nullable=True)  # Market Capitalization
    pe_ratio = db.Column(db.Float, nullable=True)  # Price-to-Earnings Ratio
    sector = db.Column(db.String(100), nullable=True)  # Sector of the company
    # Add additional fields as needed

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'market_cap': self.market_cap,
            'pe_ratio': self.pe_ratio,
            'sector': self.sector
            # Include other new fields in this method
        }
