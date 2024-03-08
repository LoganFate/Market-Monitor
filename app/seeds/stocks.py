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
        ),
        Stock(
    symbol='NVDA',
    name='NVIDIA Corporation',
    price=220.00,  # Example value
    category='Technology',
    market_cap=550000000000,  # Example value
    pe_ratio=40,  # Example value
    sector='Technology',
    previous_close=219.00  # Example value
),
Stock(
    symbol='INTC',
    name='Intel Corporation',
    price=50.00,  # Example value
    category='Technology',
    market_cap=200000000000,  # Example value
    pe_ratio=12,  # Example value
    sector='Technology',
    previous_close=49.50  # Example value
),
Stock(
    symbol='JPM',
    name='JPMorgan Chase & Co.',
    price=160.00,  # Example value
    category='Financials',
    market_cap=480000000000,  # Example value
    pe_ratio=10,  # Example value
    sector='Financials',
    previous_close=159.00  # Example value
),
Stock(
    symbol='JNJ',
    name='Johnson & Johnson',
    price=170.00,  # Example value
    category='Healthcare',
    market_cap=450000000000,  # Example value
    pe_ratio=25,  # Example value
    sector='Healthcare',
    previous_close=169.00  # Example value
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
