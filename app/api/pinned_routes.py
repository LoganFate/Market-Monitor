from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import  db, Article, User
from sqlalchemy.sql import text

pinned_routes = Blueprint('pinned', __name__)

@pinned_routes.route('/pinned', methods=['POST'])
@login_required
def pin_article():
    data = request.get_json()
    article_id = data.get('article_id')
    category = data.get('category', 'default')

    if not article_id:
        return jsonify({"error": "Article ID is required."}), 400

    article = Article.query.get(article_id)
    if not article:
        return jsonify({"error": "Article not found."}), 404

    existing_pin = db.session.execute(
        text("SELECT 1 FROM user_pinned WHERE user_id=:user_id AND article_id=:article_id"),
        {"user_id": current_user.id, "article_id": article_id}
    ).fetchone()

    if existing_pin:
        return jsonify({"error": "Article already pinned."}), 409

    db.session.execute(
        text("""
            INSERT INTO user_pinned (user_id, article_id, category)
            VALUES (:user_id, :article_id, :category)
        """),
        {"user_id": current_user.id, "article_id": article_id, "category": category}
    )
    db.session.commit()

    return jsonify({"message": "Article pinned successfully with category."}), 201


@pinned_routes.route('/pinned', methods=['GET'])
@login_required
def view_pinned_articles():
    articles_data = [{
        "id": article.id,
        "title": article.title,
        "content": article.content,
        # Add other fields as necessary
    } for article in current_user.pinned_articles]

    return jsonify(articles_data), 200

@pinned_routes.route('/pinned', methods=['DELETE'])
@login_required
def unpin_article():
    article_id = request.args.get('article_id')

    if not article_id:
        return jsonify({"error": "Article ID is required."}), 400

    article = Article.query.filter_by(id=article_id).first()
    if not article or article not in current_user.pinned_articles:
        return jsonify({"error": "Article not found in pinned articles."}), 404

    current_user.pinned_articles.remove(article)
    db.session.commit()

    return jsonify({"message": "Article unpinned successfully."}), 204
