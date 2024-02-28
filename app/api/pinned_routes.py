from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import  db, Article, User
from sqlalchemy.sql import text

pinned_routes = Blueprint('pinned', __name__)

@pinned_routes.route('/', methods=['POST'])
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


@pinned_routes.route('/', methods=['GET'])
@login_required
def view_pinned_articles():
    articles_data = [{
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "category": article.category
        # Add other fields as necessary
    } for article in current_user.pinned_articles]

    return jsonify(articles_data), 200

@pinned_routes.route('/<int:pinnedId>', methods=['DELETE'])
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

@pinned_routes.route('/<int:pinnedId>', methods=['PUT'])
@login_required
def update_pinned_article_category():
    data = request.get_json()
    article_ids = data.get('article_ids')
    new_category = data.get('new_category')

    if not article_ids or not new_category:
        return jsonify({"error": "Article IDs and new category are required."}), 400

    for article_id in article_ids:

        sql = text("""
            UPDATE user_pinned
            SET category = :new_category
            WHERE user_id = :user_id AND article_id = :article_id
        """)
        db.engine.execute(sql, new_category=new_category, user_id=current_user.id, article_id=article_id)

    db.session.commit()

    return jsonify({"message": "Article categories updated successfully."}), 200
