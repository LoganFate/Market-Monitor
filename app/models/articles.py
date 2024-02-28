from .db import db, environment, SCHEMA, add_prefix_for_prod


class Article(db.Model):
    __tablename__ = 'articles'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    # Add other fields as necessary, such as publication_date, category, etc.


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'category': self.category
            # Include other fields if necessary after integrating polygon API
        }
