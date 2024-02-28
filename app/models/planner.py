from .db import db, environment, SCHEMA, add_prefix_for_prod


class PlannerEntry(db.Model):
    __tablename__ = 'planner_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Daily, Weekly, Monthly
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('planner_entries', lazy=True))
