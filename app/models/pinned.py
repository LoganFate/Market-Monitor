from .db import db, environment, SCHEMA, add_prefix_for_prod

class Pinned(db.Model):
    __tablename__ = 'pinned'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('articles.id')), nullable=False)
    category = db.Column(db.String(50), nullable=True)

    user_pinned = db.relationship('User', backref=db.backref('pinned_articles', lazy=True))
    article = db.relationship('Article', backref=db.backref('pinned_by_users', lazy=True))


def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'article_id': self.stock_id,
            'category': self.category
        }
