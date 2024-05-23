from app import db

class RealEstate(db.Model):
    __tablename__ = 'real_estate'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float, nullable=False)

    def __init__(self, address, price, area):
        self.address = address
        self.price = price
        self.area = area

    def __repr__(self):
        return f'<RealEstate {self.address}>'
