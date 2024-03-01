from datetime import datetime
from app.models import db, environment, SCHEMA, Comment
from sqlalchemy.sql import text


def seed_comments():
    comments_data = [
        Comment(user_id=1, article_id='1', text='Interesting article.', created_at=datetime.now()),
        Comment(user_id=2, article_id='2', text='This was very informative.', created_at=datetime.now()),
        Comment(user_id=3, article_id='3', text='I have a question about this.', created_at=datetime.now()),
        Comment(user_id=4, article_id='4', text='Glad I read this, thanks for posting.', created_at=datetime.now()),
        Comment(user_id=5, article_id='5', text='Looking forward to more articles like this.', created_at=datetime.now()),
    ]

    db.session.bulk_save_objects(comments_data)
    db.session.commit()

def undo_comments():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.comments RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM comments"))
    db.session.commit()
