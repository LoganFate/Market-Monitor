from app.models import db, Stock, environment, SCHEMA
from sqlalchemy.sql import text
import os

# Define your stock data here
# Define your stock data here
def seed_stocks():
    # Example stocks
    stocks = [
        Stock(
            symbol='AAPL',
            name='Apple Inc.',
            price=150.00,
            category='Technology',
            market_cap=2000000000000,
            pe_ratio=30,
            sector='Technology',
            previous_close=149.10  # Example value
        ),
        Stock(
            symbol='MSFT',
            name='Microsoft Corporation',
            price=250.00,
            category='Technology',
            market_cap=1800000000000,
            pe_ratio=35,
            sector='Technology',
            previous_close=249.68  # Example value
        ),
        Stock(
            symbol='GOOGL',
            name='Alphabet Inc.',
            price=2800.00,
            category='Technology',
            market_cap=1500000000000,
            pe_ratio=25,
            sector='Technology',
            previous_close=2799.72  # Example value
        ),
        Stock(
            symbol='AMZN',
            name='Amazon.com, Inc.',
            price=3200.00,
            category='E-commerce',
            market_cap=1600000000000,
            pe_ratio=60,
            sector='Consumer Discretionary',
            previous_close=3199.95  # Example value
        ),
        Stock(
            symbol='TSLA',
            name='Tesla, Inc.',
            price=700.00,
            category='Automotive',
            market_cap=700000000000,
            pe_ratio=110,
            sector='Consumer Discretionary',
            previous_close=699.60  # Example value
        )
    ]

    db.session.bulk_save_objects(stocks)
    db.session.commit()


# Function to undo the seeding
def undo_stocks():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.stocks RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM stocks"))
    db.session.commit()

if __name__ == '__main__':
    seed_stocks()
