from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import  db, Article, Pinned
from sqlalchemy.sql import text
from datetime import datetime

pinned_routes = Blueprint('pinned', __name__)

@pinned_routes.route('', methods=['POST'])
@login_required
def pin_article():
    data = request.get_json()
    title = data.get('title')  # Assuming you're sending the title
    article_id = data.get('article_id')
    category = data.get('category', 'default')

    # Attempt to fetch the article by title
    article = Article.query.filter_by(id=article_id).first() if article_id else Article.query.filter_by(title=title).first()

    # If the article does not exist, create a new article object with the given details
    if not article and article_id:
        article = Article(
            id=article_id,
            title=title,
            content=data.get('content', ''),  # Default to empty string if content is not provided
            author=data.get('author', ''),  # Default to empty string if author is not provided
            article_url=data.get('article_url', ''),  # Default to empty string if article_url is not provided
            image_url=data.get('image_url', ''),  # Default to empty string if image_url is not provided
            published_utc=datetime.strptime(data.get('published_utc'), '%Y-%m-%dT%H:%M:%SZ') if data.get('published_utc') else None,  # Handle date conversion
            publisher=data.get('publisher', '{}')  # Default to empty string if publisher is not provided
        )
        db.session.add(article)
        db.session.commit()
        article = article  # Assign the newly created article for pinning

    # If article_id is not provided in the request, it's an error
    if not article_id:
        return jsonify({"error": "Article ID is required."}), 400

    article = Article.query.get(article_id)
    if not article:
        return jsonify({"error": "Article not found."}), 404

    existing_pin = db.session.execute(
        text("SELECT 1 FROM pinned WHERE user_id=:user_id AND article_id=:article_id"),
        {"user_id": current_user.id, "article_id": article_id}
    ).fetchone()

    if existing_pin:
        return jsonify({"error": "Article already pinned."}), 409

    db.session.execute(
        text("""
            INSERT INTO pinned (user_id, article_id, category)
            VALUES (:user_id, :article_id, :category)
        """),
        {"user_id": current_user.id, "article_id": article_id, "category": category}
    )
    db.session.commit()

    return jsonify({"message": "Article pinned successfully with category."}), 201


@pinned_routes.route('', methods=['GET'])
@login_required
def view_pinned_articles():
 articles_data = []

 for pinned in current_user.pinned_articles:
        article = pinned.article
        if article:
            articles_data.append({
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "category": article.category
                # Add other fields as necessary from the Article model
            })
        else:
            print(f"Pinned entry {pinned.id} has no associated article.")

 return jsonify(articles_data), 200

@pinned_routes.route('', methods=['DELETE'])
@login_required
def unpin_article():
   data = request.get_json()
   article_id = data.get('article_id')

   if not article_id:
        return jsonify({"error": "Article ID is required."}), 400


   pinned_entry = Pinned.query.filter_by(user_id=current_user.id, article_id=article_id).first()

   if not pinned_entry:
        return jsonify({"error": "Article not found in pinned articles."}), 404


   db.session.delete(pinned_entry)
   db.session.commit()

   return jsonify({"message": "Article unpinned successfully."}), 204

@pinned_routes.route('', methods=['PUT'])
@login_required
def update_pinned_article_category():
    data = request.get_json()
    article_id = data.get('article_id')
    category = data.get('category')


    if not article_id or not category:
        return jsonify({"error": "Article ID and new category are required."}), 400


    updated_entry = Pinned.query.filter_by(user_id=current_user.id, article_id=article_id).update({'category': category}, synchronize_session=False)


    if updated_entry == 0:
        return jsonify({"error": "No pinned article found with the provided article ID"}), 404


    try:
        db.session.commit()
        return jsonify({"message": "Pinned article category updated successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update pinned article category. Error: {str(e)}"}), 500
