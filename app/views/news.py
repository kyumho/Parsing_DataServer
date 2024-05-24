from flask import Flask, Blueprint, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote

# 환경변수 로드
load_dotenv()

app = Flask(__name__)

news_bp = Blueprint('news', __name__)

CLIENT_ID = os.getenv('CLIENT_ID')  # Naver API Client ID
CLIENT_SECRET = os.getenv('CLIENT_SECRET')  # Naver API Client Secret

@news_bp.route('/')
def display_news():
    return render_template('news.html')


@news_bp.route('/search', methods=['POST'])
def search_news():
    query = request.json.get('query')
    raw_data = fetch_news(query)
    print(raw_data)
    processed_data = process_news(raw_data)
    return jsonify(processed_data)


def fetch_news(keyword):
    encoded_keyword = quote(keyword)  # 키워드를 UTF-8로 인코딩
    url = f"https://openapi.naver.com/v1/search/news.json?query={encoded_keyword}&display=10&start=1&sort=sim"
    headers = {
        'X-Naver-Client-Id': CLIENT_ID,
        'X-Naver-Client-Secret': CLIENT_SECRET
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(response.content)
        return {}


def process_news(raw_data):
    processed_data = [{"title": item["title"], "description": item["description"], "link": item["link"]}
                      for item in raw_data.get('items', [])]
    return processed_data


