from flask import Blueprint, jsonify
from app.models import  db, Article

article_routes = Blueprint('articles', __name__)

@article_routes.route('/', methods=['GET'])
def get_articles():
    """
    User will be able to view articles on the site.
    """
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles]), 200
