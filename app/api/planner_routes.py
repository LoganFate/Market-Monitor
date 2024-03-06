from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Planner

planner_routes = Blueprint('planner', __name__, url_prefix='/api/planner')

@planner_routes.route('', methods=['POST'])
@login_required
def add_plan():
    data = request.get_json()
    planner_category = data.get('planner_category')
    plan_text = data.get('plan_text')


    if not planner_category or not plan_text:
        return jsonify({"error": "Missing planner category or plan text"}), 400


    new_plan = Planner(
        user_id=current_user.id,
        category=planner_category,
        text=plan_text
    )


    db.session.add(new_plan)
    db.session.commit()

    return jsonify(new_plan.to_dict()), 201

@planner_routes.route('', methods=['GET'])
@login_required
def view_plans():

    plans = Planner.query.filter_by(user_id=current_user.id).all()


    plans_data = [plan.to_dict() for plan in plans]

    return jsonify(plans_data), 200

@planner_routes.route('/<int:plan_id>', methods=['PUT'])
@login_required
def update_plan(plan_id):
    data = request.get_json()
    planner_category = data.get('planner_category')
    plan_text = data.get('plan_text')


    plan = Planner.query.filter_by(id=plan_id, user_id=current_user.id).first()

    if not plan:
        return jsonify({"error": "Plan not found"}), 404


    if planner_category:
        plan.category = planner_category
    if plan_text:
        plan.text = plan_text



    db.session.commit()

    return jsonify(plan.to_dict()), 200

@planner_routes.route('/<int:plan_id>', methods=['DELETE'])
@login_required
def delete_plan(plan_id):

    plan = Planner.query.filter_by(id=plan_id, user_id=current_user.id).first()

    if not plan:
        return jsonify({"error": "Plan not found"}), 404

    db.session.delete(plan)
    db.session.commit()

    return jsonify({"message": "Plan deleted successfully"}), 204
