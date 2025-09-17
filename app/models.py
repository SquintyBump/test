from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    author = db.Column(db.String(128), index=True)
    status = db.Column(db.String(64), index=True, default='wanted')
    download_id = db.Column(db.String(128), index=True, nullable=True)

    def __repr__(self):
        return f'<Book {self.title}>'


class Indexer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(128), unique=True)
    api_key = db.Column(db.String(128))
    indexer_type = db.Column(db.String(64), default='Torznab')

    def __repr__(self):
        return f'<Indexer {self.name}>'


class DownloadClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    client_type = db.Column(db.String(64), default='qBittorrent')
    host = db.Column(db.String(128))
    port = db.Column(db.Integer)
    username = db.Column(db.String(64))
    password = db.Column(db.String(128))  # In a real app, this should be encrypted

    def __repr__(self):
        return f'<DownloadClient {self.name}>'
