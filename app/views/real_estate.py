from flask import Blueprint, render_template
from app.models.real_estate import RealEstate, db
import requests

real_estate_bp = Blueprint('real_estate', __name__)


@real_estate_bp.route('/')
def display_real_estate_info():
    real_estate_data = fetch_real_estate_data()
    analyzed_data = analyze_real_estate_data(real_estate_data)
    save_real_estate_data(analyzed_data['details'])
    return render_template('real_estate.html', data=analyzed_data)


def fetch_real_estate_data():
    url = "http://example.com/api/real_estate"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def analyze_real_estate_data(data):
    if not data:
        return {}

    total_price = sum(item['price'] for item in data)
    average_price = total_price / len(data) if len(data) > 0 else 0

    return {
        "total_properties": len(data),
        "average_price": average_price,
        "details": data
    }


def save_real_estate_data(data):
    for item in data:
        existing_property = RealEstate.query.filter_by(address=item['address']).first()
        if not existing_property:
            new_property = RealEstate(
                address=item['address'],
                price=item['price'],
                area=item['area']
            )
            db.session.add(new_property)
    db.session.commit()
