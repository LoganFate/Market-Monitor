from app.models import db, Planner, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime


def seed_planner():
    planner_entries = [
        Planner(user_id=1, category='Daily', text='Daily planner entry for User 1', created_at=datetime.now()),
        Planner(user_id=2, category='Weekly', text='Weekly planner entry for User 2', created_at=datetime.now()),
        Planner(user_id=3, category='Monthly', text='Monthly planner entry for User 3', created_at=datetime.now()),
        Planner(user_id=4, category='Daily', text='Another daily planner entry for User 4', created_at=datetime.now()),
        Planner(user_id=5, category='Weekly', text='Another weekly planner entry for User 5', created_at=datetime.now()),
    ]

    db.session.bulk_save_objects(planner_entries)
    db.session.commit()

def undo_planner():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.planner RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM planner"))
    db.session.commit()
