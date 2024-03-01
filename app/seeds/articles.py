from app.models import db, Article, environment, SCHEMA
from sqlalchemy.sql import text


def seed_articles():
    articles_data = [
        Article(title='The Future of Technology', content='Content about technology...', author='Jane Doe', category='Tech'),
        Article(title='Finance Trends 2024', content='Content about finance...', author='John Smith', category='Finance'),
        Article(title='Healthcare Innovations', content='Content about healthcare...', author='Alex Johnson', category='Healthcare'),
        Article(title='Renewable Energy Sources', content='Content about energy...', author='Chris Lee', category='Energy'),
        Article(title='The Rise of Consumer Goods', content='Content about consumer goods...', author='Pat Kim', category='Consumer Goods'),
    ]

    db.session.bulk_save_objects(articles_data)
    db.session.commit()

def undo_articles():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.articles RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM articles"))
    db.session.commit()
