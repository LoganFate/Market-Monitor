from flask import Blueprint, jsonify, request
from app.models import  db, Article
from datetime import datetime
from sqlalchemy.exc import IntegrityError


article_routes = Blueprint('articles', __name__)

@article_routes.route('/', methods=['GET'])
def get_articles():
    """
    User will be able to view articles on the site.
    """
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles]), 200

@article_routes.route('/', methods=['POST'])
def add_articles():
    articles_data = request.get_json().get('articles', [])

    if not articles_data:
        return jsonify({"error": "No articles data provided."}), 400

    new_articles = []
    for article_data in articles_data:
        # Check if the article already exists
        existing_article = Article.query.get(article_data.get('id'))
        if existing_article is None:
            try:
                new_article = Article(
                    id=article_data.get('id'),
                    title=article_data.get('title'),
                    content=article_data.get('description', ''),  # Assuming you map 'content' to 'description'
                    author=article_data.get('author'),
                    article_url=article_data.get('article_url'),
                    image_url=article_data.get('image_url'),
                    published_utc=datetime.strptime(article_data.get('published_utc'), "%Y-%m-%dT%H:%M:%SZ") if article_data.get('published_utc') else None,
                    # Handle 'publisher' accordingly
                )
                db.session.add(new_article)
                db.session.commit()
                new_articles.append(new_article.to_dict())  # Ensure your model has a to_dict method
            except IntegrityError as e:
                db.session.rollback()
                # Log the error or handle it accordingly
                print(f"Error adding article {article_data.get('id')}: {e}")

    if new_articles:
        return jsonify(new_articles), 201
    else:
        return jsonify({"error": "No new articles were added. Articles may already exist."}), 200
