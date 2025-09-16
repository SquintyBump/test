from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    author = db.Column(db.String(128), index=True)
    status = db.Column(db.String(64), index=True, default='wanted')

    def __repr__(self):
        return f'<Book {self.title}>'
