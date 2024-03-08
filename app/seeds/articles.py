from app.models import db, Article, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime
import json


def seed_articles():
    articles_data = [
        Article(
            id="1",
            title='The Future of Technology',
            content='Content about technology...',
            author='Jane Doe',
            article_url='http://example.com/future-of-technology',
            image_url='http://example.com/images/future-of-technology.jpg',
            published_utc=datetime.utcnow(),
            publisher=json.dumps({"name": "TechCrunch", "homepage_url": "https://techcrunch.com"})
        ),
        Article(
            id="2",
            title='Finance Trends 2024',
            content='Content about finance...',
            author='John Smith',
            article_url='http://example.com/finance-trends-2024',
            image_url='http://example.com/images/finance-trends-2024.jpg',
            published_utc=datetime.utcnow(),
            publisher=json.dumps({"name": "Bloomberg", "homepage_url": "https://www.bloomberg.com"})
        ),
        Article(
            id="3",
            title='Healthcare Innovations',
            content='Content about healthcare...',
            author='Alex Johnson',
            article_url='http://example.com/healthcare-innovations',
            image_url='http://example.com/images/healthcare-innovations.jpg',
            published_utc=datetime.utcnow(),
            publisher=json.dumps({"name": "Health News", "homepage_url": "https://www.healthnews.com"})
        ),
        Article(
            id="4",
            title='Renewable Energy Sources',
            content='Content about energy...',
            author='Chris Lee',
            article_url='http://example.com/renewable-energy-sources',
            image_url='http://example.com/images/renewable-energy-sources.jpg',
            published_utc=datetime.utcnow(),
            publisher=json.dumps({"name": "Energy Today", "homepage_url": "https://www.energytoday.com"})
        ),
        Article(
            id="5",
            title='The Rise of Consumer Goods',
            content='Content about consumer goods...',
            author='Pat Kim',
            article_url='http://example.com/rise-of-consumer-goods',
            image_url='http://example.com/images/rise-of-consumer-goods.jpg',
            published_utc=datetime.utcnow(),
            publisher=json.dumps({"name": "Consumer Reports", "homepage_url": "https://www.consumerreports.org"})
        ),
    ]

    for article_data in articles_data:
        # Check if an article with the same ID already exists
        existing_article = Article.query.filter_by(id=article_data.id).first()
        if not existing_article:
            db.session.add(article_data)
    try:
        db.session.commit()
    except Exception as e:
        print(f"An error occurred while seeding articles: {e}")
        db.session.rollback()

def undo_articles():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.articles RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM articles"))
    db.session.commit()
