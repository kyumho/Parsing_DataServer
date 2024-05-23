from flask import Blueprint, render_template
import requests

news_bp = Blueprint('news', __name__)


@news_bp.route('/')
def display_news():
    raw_data = fetch_news()
    processed_data = process_news(raw_data)
    return render_template('news.html', data=processed_data)


def fetch_news():
    url = "http://example.com/api/news"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def process_news(raw_data):
    processed_data = [{"title": item["title"], "summary": item["summary"]} for item in raw_data]
    return processed_data
