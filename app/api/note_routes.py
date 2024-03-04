from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Note, Stock

note_routes = Blueprint('note', __name__, url_prefix='/api/notes')

@note_routes.route('', methods=['POST'])
@login_required
def add_note():
    data = request.get_json()
    stock_id = data.get('stock_id')
    note_text = data.get('note_text')


    if not stock_id or not note_text:
        return jsonify({"error": "Missing stock ID or note text"}), 400


    stock = Stock.query.get(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found"}), 404


    new_note = Note(
        user_id=current_user.id,
        stock_id=stock_id,
        text=note_text
    )

    # Add the new note to the database
    db.session.add(new_note)
    db.session.commit()

    return jsonify(new_note.to_dict()), 201

@note_routes.route('/<int:stock_id>', methods=['GET'])
@login_required
def view_notes(stock_id):

    stock = Stock.query.get(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    # Retrieve all notes for the current user and specified stock
    notes = Note.query.filter_by(user_id=current_user.id, stock_id=stock_id).all()

    # Convert each note to its dictionary representation
    notes_data = [note.to_dict() for note in notes]

    return jsonify(notes_data), 200


@note_routes.route('/<int:note_id>', methods=['PUT'])
@login_required
def edit_note(note_id):
    data = request.get_json()
    note_text = data.get('note_text')

    # Validate input
    if not note_text:
        return jsonify({"error": "Missing note text"}), 400

    # Ensure the note exists and belongs to the current user
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({"error": "Note not found"}), 404

    # Update the note's text
    note.text = note_text
    db.session.commit()

    return jsonify({"message": "Note updated successfully"}), 200

@note_routes.route('/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    # Ensure the note exists and belongs to the current user
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({"error": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()

    return '', 204
