from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declared_attr


user_pinned = db.Table('user_pinned',
    db.Column('user_id', db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), primary_key=True),
    db.Column('article_id', db.String(255), db.ForeignKey(add_prefix_for_prod('articles.id')), primary_key=True),
)
user_watchlist = db.Table('user_watchlist',
    db.Column('user_id', db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), primary_key=True),
    db.Column('stock_id', db.Integer, db.ForeignKey(add_prefix_for_prod('stocks.id')), primary_key=True),
    db.Column('category', db.String(50))
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    user_about = db.Column(db.Text, nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True, default='default_profile_pic_url_or_path_here')

    watchlist_stocks = db.relationship('Stock', secondary=user_watchlist,
                                       backref=db.backref('watchlisted_by', lazy='dynamic'))
    pinned_articles = db.relationship('Article', secondary=user_pinned,
                                       backref=db.backref('pinned_by', lazy='dynamic'))


    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'user_about': self.user_about,
            'profile_pic': self.profile_pic
        }
