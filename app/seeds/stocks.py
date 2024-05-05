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
),
Stock(
            symbol='BAC',
            name='Bank of America Corp',
            price=30.50,
            category='Financials',
            market_cap=250000000000,
            pe_ratio=12,
            sector='Financials',
            previous_close=30.00
        ),
        Stock(
            symbol='NFLX',
            name='Netflix Inc',
            price=350.00,
            category='Communication Services',
            market_cap=154000000000,
            pe_ratio=50,
            sector='Communication Services',
            previous_close=348.30
        ),
        Stock(
            symbol='V',
            name='Visa Inc',
            price=210.00,
            category='Financials',
            market_cap=450000000000,
            pe_ratio=35,
            sector='Financials',
            previous_close=208.90
        ),
        Stock(
            symbol='MA',
            name='Mastercard Incorporated',
            price=330.00,
            category='Financials',
            market_cap=330000000000,
            pe_ratio=40,
            sector='Financials',
            previous_close=329.00
        ),
        Stock(
            symbol='DIS',
            name='Walt Disney Co',
            price=120.00,
            category='Communication Services',
            market_cap=220000000000,
            pe_ratio=28,
            sector='Communication Services',
            previous_close=119.00
        ),
        Stock(
            symbol='PG',
            name='Procter & Gamble Co',
            price=140.00,
            category='Consumer Staples',
            market_cap=340000000000,
            pe_ratio=24,
            sector='Consumer Staples',
            previous_close=138.50
        ),
        Stock(
            symbol='KO',
            name='Coca-Cola Co',
            price=60.00,
            category='Consumer Staples',
            market_cap=260000000000,
            pe_ratio=30,
            sector='Consumer Staples',
            previous_close=59.50
        ),
        Stock(
            symbol='NKE',
            name='Nike Inc',
            price=110.00,
            category='Consumer Discretionary',
            market_cap=170000000000,
            pe_ratio=35,
            sector='Consumer Discretionary',
            previous_close=109.00
        ),
        Stock(
            symbol='MRK',
            name='Merck & Co Inc',
            price=80.00,
            category='Healthcare',
            market_cap=200000000000,
            pe_ratio=20,
            sector='Healthcare',
            previous_close=79.50
        ),
        Stock(
            symbol='PFE',
            name='Pfizer Inc',
            price=40.00,
            category='Healthcare',
            market_cap=220000000000,
            pe_ratio=10,
            sector='Healthcare',
            previous_close=39.90
        ),
        Stock(
            symbol='CVX',
            name='Chevron Corporation',
            price=150.00,
            category='Energy',
            market_cap=290000000000,
            pe_ratio=15,
            sector='Energy',
            previous_close=148.50
        ),
        Stock(
            symbol='XOM',
            name='Exxon Mobil Corporation',
            price=100.00,
            category='Energy',
            market_cap=350000000000,
            pe_ratio=18,
            sector='Energy',
            previous_close=99.00
        ),
         Stock(
            symbol='PINS',
            name='Pinterest, Inc.',
            price=22.00,
            category='Technology',
            market_cap=12000000000,
            pe_ratio=35,
            sector='Communication Services',
            previous_close=21.90
        ),
        Stock(
            symbol='SNAP',
            name='Snap Inc.',
            price=14.00,
            category='Technology',
            market_cap=20000000000,
            pe_ratio=50,
            sector='Communication Services',
            previous_close=13.85
        ),

        Stock(
            symbol='ZM',
            name='Zoom Video Communications, Inc.',
            price=110.00,
            category='Technology',
            market_cap=30000000000,
            pe_ratio=90,
            sector='Information Technology',
            previous_close=108.90
        ),
        Stock(
            symbol='CRM',
            name='Salesforce, Inc.',
            price=170.00,
            category='Technology',
            market_cap=160000000000,
            pe_ratio=85,
            sector='Information Technology',
            previous_close=168.50
        ),


        Stock(
            symbol='SPOT',
            name='Spotify Technology S.A.',
            price=122.00,
            category='Technology',
            market_cap=23000000000,
            pe_ratio=-15,
            sector='Communication Services',
            previous_close=120.50
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
