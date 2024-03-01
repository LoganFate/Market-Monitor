from datetime import datetime
from app.models import db, environment, SCHEMA, Note
from sqlalchemy.sql import text

def seed_notes():
    notes_data = [
        Note(user_id=1, stock_id=1, text='Note 1 for User 1 on Stock 1', created_at=datetime.now()),
        Note(user_id=2, stock_id=2, text='Note 2 for User 2 on Stock 2', created_at=datetime.now()),
        Note(user_id=3, stock_id=3, text='Note 3 for User 3 on Stock 3', created_at=datetime.now()),
        Note(user_id=4, stock_id=4, text='Note 4 for User 4 on Stock 4', created_at=datetime.now()),
        Note(user_id=5, stock_id=5, text='Note 5 for User 5 on Stock 5', created_at=datetime.now()),
    ]

    db.session.bulk_save_objects(notes_data)
    db.session.commit()

def undo_notes():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.notes RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM notes"))
    db.session.commit()
