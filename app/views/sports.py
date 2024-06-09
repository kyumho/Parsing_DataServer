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
        events = extract_event_data(odds_data)
        return jsonify(events)
    else:
        return jsonify({'error': 'Failed to fetch odds'}), response.status_code


def extract_event_data(data):
    events = []
    for event in data:
        event_info = {
            "id": event.get('id'),
            "sport_key": event.get('sport_key'),
            "sport_title": event.get('sport_title'),
            "commence_time": event.get('commence_time'),
            "home_team": event.get('home_team'),
            "away_team": event.get('away_team'),
            "bookmakers": []
        }
        for bookmaker in event['bookmakers']:
            bookmaker_info = {
                "key": bookmaker.get('key'),
                "title": bookmaker.get('title'),
                "last_update": bookmaker.get('last_update'),
                "markets": []
            }
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':
                    market_info = {
                        "key": market.get('key'),
                        "last_update": market.get('last_update'),
                        "outcomes": []
                    }
                    for outcome in market['outcomes']:
                        outcome_info = {
                            "name": outcome.get('name'),
                            "price": outcome.get('price')
                        }
                        market_info['outcomes'].append(outcome_info)
                    bookmaker_info['markets'].append(market_info)
            event_info['bookmakers'].append(bookmaker_info)
        events.append(event_info)
    return events
