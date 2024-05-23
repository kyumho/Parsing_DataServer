from app import db

class MapData(db.Model):
    __tablename__ = 'map_data'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    data = db.Column(db.JSON, nullable=False)

    def __init__(self, location, data):
        self.location = location
        self.data = data

    def __repr__(self):
        return f'<MapData {self.location}>'