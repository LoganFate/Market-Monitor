from .db import db, environment, SCHEMA, add_prefix_for_prod



class Article(db.Model):
    __tablename__ = 'articles'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}


    id = db.Column(db.String(500), primary_key=True)  # Assuming id from API is unique
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)  # You might want to map this to 'description' from the API data
    author = db.Column(db.String(100), nullable=True)
    article_url = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    published_utc = db.Column(db.DateTime, nullable=True)
    publisher = db.Column(db.JSON, nullable=True)
    category = db.Column(db.String(255), nullable=True)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'article_url': self.article_url,
            'image_url': self.image_url,
            'published_utc': self.published_utc.isoformat() if self.published_utc else None,
            'publisher': self.publisher,  # This will return the JSON object/dict as is
            'category': self.category
        }
