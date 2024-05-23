from flask import Blueprint, render_template
from app.models.sports import SportsOdds
import requests

sports_bp = Blueprint('sports', __name__)

@sports_bp.route('/')
def display_sports_odds():
    odds_data = fetch_sports_odds()
    probabilities = calculate_probabilities(odds_data)
    return render_template('sports.html', data=probabilities)

def fetch_sports_odds():
    url = "http://example.com/api/sports_odds"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def calculate_probabilities(data):
    # 확률 계산 로직
    probabilities = [{"team": item["team"], "probability": item["odds"] / 100} for item in data]
    return probabilities