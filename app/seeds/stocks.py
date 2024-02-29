from app.models import db, Stock, environment, SCHEMA
from sqlalchemy.sql import text

# Define your stock data here
# Define your stock data here
def seed_stocks():
    # Example stocks
    stock1 = Stock(
        symbol='AAPL',
        name='Apple Inc.',
        price=150.00,
        category='Technology',
        market_cap=2000000000000,
        pe_ratio=30,
        sector='Technology',
        previous_close=None  # Add this field and set it to None initially
        # Add other fields as needed
    )
    stock2 = Stock(
        symbol='MSFT',
        name='Microsoft Corporation',
        price=250.00,
        category='Technology',
        market_cap=1800000000000,
        pe_ratio=35,
        sector='Technology',
        previous_close=None  # Add this field and set it to None initially
        # Add other fields as needed
    )
    stock3 = Stock(
        symbol='GOOGL',
        name='Alphabet Inc.',
        price=2800.00,
        category='Technology',
        market_cap=1500000000000,
        pe_ratio=25,
        sector='Technology',
        previous_close=None  # Add this field and set it to None initially
        # Add other fields as needed
    )

    # Add stocks to session
    db.session.add(stock1)
    db.session.add(stock2)
    db.session.add(stock3)

    # Commit to save changes to the database
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
