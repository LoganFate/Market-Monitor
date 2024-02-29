from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Comment, Article

comment_routes = Blueprint('comment', __name__, url_prefix='/api/comments')

@comment_routes.route('', methods=['POST'])
@login_required
def add_comment():
    data = request.get_json()
    article_id = data.get('article_id')
    comment_text = data.get('comment_text')

    if not article_id or not comment_text:
        return jsonify({"error": "Missing article ID or comment text"}), 400

    new_comment = Comment(
        user_id=current_user.id,
        article_id=article_id,
        text=comment_text
    )

    db.session.add(new_comment)
    db.session.commit()

    return jsonify(new_comment.to_dict()), 201

@comment_routes.route('/<article_id>', methods=['GET'])
@login_required
def view_comments(article_id):
    comments = Comment.query.filter_by(article_id=article_id).all()
    comments_data = [comment.to_dict() for comment in comments]

    return jsonify(comments_data), 200

@comment_routes.route('/<int:comment_id>', methods=['PUT'])
@login_required
def edit_comment(comment_id):
    data = request.get_json()
    comment_text = data.get('comment_text')

    comment = Comment.query.filter_by(id=comment_id, user_id=current_user.id).first()
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    comment.text = comment_text
    db.session.commit()

    return jsonify({"message": "Comment updated successfully"}), 200


@comment_routes.route('/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id, user_id=current_user.id).first()
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    db.session.delete(comment)
    db.session.commit()

    return '', 204
