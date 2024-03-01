from app.models import db, Pinned, environment, SCHEMA
from sqlalchemy.sql import text


def seed_pinned():
    pinned_items = [
        Pinned(user_id=1, article_id='1', category='Tech'),
        Pinned(user_id=2, article_id='2', category='Finance'),
        Pinned(user_id=3, article_id='3', category='Healthcare'),
        Pinned(user_id=4, article_id='4', category='Energy'),
        Pinned(user_id=5, article_id='5', category='Consumer Goods'),
    ]

    db.session.bulk_save_objects(pinned_items)
    db.session.commit()

def undo_pinned():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.pinned RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM pinned"))

    db.session.commit()
