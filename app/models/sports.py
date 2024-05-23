from app import db

class SportsOdds(db.Model):
    __tablename__ = 'sports_odds'

    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(255), nullable=False)
    odds = db.Column(db.Float, nullable=False)

    def __init__(self, team, odds):
        self.team = team
        self.odds = odds

    def __repr__(self):
        return f'<SportsOdds {self.team}>'