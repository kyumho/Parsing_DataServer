from flask import Blueprint, render_template
from app.models.maps import MapData
import requests

maps_bp = Blueprint('maps', __name__)


@maps_bp.route('/')
def display_map():
    map_data = fetch_map_data()
    generated_map = generate_map(map_data)
    return render_template('maps.html', map=generated_map)


def fetch_map_data():
    url = "http://example.com/api/maps"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def generate_map(data):
    # 지도 생성 로직
    return {"generated_map_url": "http://example.com/generated_map.png"}
