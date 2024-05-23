from app import db

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)

    def __init__(self, title, summary):
        self.title = title
        self.summary = summary

    def __repr__(self):
        return f'<News {self.title}>'