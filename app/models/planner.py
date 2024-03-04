from .db import db, environment, SCHEMA, add_prefix_for_prod

class Planner(db.Model):
    __tablename__ = 'planner'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Daily, Weekly, Monthly
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('planner_entries', lazy=True))


    def to_dict(self):

        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
        }
