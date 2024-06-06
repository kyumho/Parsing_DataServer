from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv
import requests
import os


REGIONS = 'us'
MARKETS = 'h2h'
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'

# 환경변수 로드
load_dotenv()

sports_bp = Blueprint('sports', __name__)

SPORT_ODDS_API_KEY = os.getenv('SPORT_ODDS_API_KEY')  # SPORT_ODDS_API_KEY( 배당률 정보 조회 키 )


@sports_bp.route('/')
def display_sports_odds():
    return render_template('sports.html')


@sports_bp.route('/fetch-odds')
def fetch_sports_odds():
    league = request.args.get('league')

    url = f'https://api.the-odds-api.com/v4/sports/{league}/odds'
    params = {
        'apiKey': SPORT_ODDS_API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'dateFormat': DATE_FORMAT,
        'oddsFormat': ODDS_FORMAT,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        odds_data = response.json()
        print(odds_data)
        probabilities = calculate_probabilities(odds_data)
        return jsonify(probabilities)
    else:
        return jsonify({'error': 'Failed to fetch odds'}), response.status_code


def calculate_probabilities(data):
    probabilities = []
    for event in data:
        for bookmaker in event['bookmakers']:
            for market in bookmaker['markets']:
                for outcome in market['outcomes']:
                    probabilities.append({
                        "team": outcome["name"],
                        "probability": outcome["price"]
                    })
    return probabilities
