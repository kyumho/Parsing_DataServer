import json

from flask import Blueprint, render_template, request, jsonify
from app.models.real_estate import RealEstate, db
import os
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET

# 환경변수 로드
load_dotenv()

real_estate_bp = Blueprint('real_estate', __name__)

REAL_ESTATE_CD_KEY = os.getenv('REAL_ESTATE_CD_KEY')  # REAL_ESTATE_CD_KEY( 공공데이터포탈 법정동코드 키 )
REAL_ESTATE_TRADE_KEY = os.getenv('REAL_ESTATE_TRADE_KEY')


@real_estate_bp.route('/')
def display_real_estate_info():
    return render_template('real_estate.html')


@real_estate_bp.route('/fetch_real_estate', methods=['POST'])
def fetch_and_display_real_estate_info():
    data = request.json
    region = data.get('region')
    deal_ymd = data.get('dealYmd')
    print(f"지역: {region}, 계약년월: {deal_ymd}")

    lawd_cd = get_lawd_cd(region)  # 지역명을 법정동 코드로 변환하는 함수

    print(lawd_cd)

    if not lawd_cd:
        return jsonify({"error": "Unknown region"}), 400

    region_cd_full = lawd_cd.get('StanReginCd')[1]['row'][0]['region_cd']
    region_cd_short = region_cd_full[:5]

    print(f"전체 region_cd: {region_cd_full}, 잘라낸 region_cd: {region_cd_short}")

    real_estate_data = fetch_real_estate_data(region_cd_short, deal_ymd)

    print(real_estate_data)

    # print(real_estate_data)

    # analyzed_data = analyze_real_estate_data(real_estate_data)
    # return render_template('real_estate.html', data=analyzed_data)


def fetch_real_estate_data(region_cd_short, deal_ymd):
    url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
    params = {
        'ServiceKey': REAL_ESTATE_TRADE_KEY,
        'LAWD_CD': region_cd_short,
        'DEAL_YMD': deal_ymd,
        'pageNo': '1',
        'numOfRows': '2'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print(response.text)
    else:
        return []


def parse_xml_response(xml_str):
    root = ET.fromstring(xml_str)
    result = []
    for item in root.findall('.//item'):
        data = {}
        for child in item:
            data[child.tag] = child.text
        result.append(data)
    return result


def analyze_real_estate_data(data):
    if not data:
        return {}

    total_price = sum(item['거래금액'] for item in data['response']['body']['items']['item'])
    average_price = total_price / len(data['response']['body']['items']['item']) if len(
        data['response']['body']['items']['item']) > 0 else 0

    return {
        "total_properties": len(data['response']['body']['items']['item']),
        "average_price": average_price,
        "details": data['response']['body']['items']['item']
    }


def get_lawd_cd(region_name):
    url = 'http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList'
    params = {
        'serviceKey': REAL_ESTATE_CD_KEY,
        'type': 'json',
        'pageNo': '1',
        'numOfRows': '1',
        'locatadd_nm': region_name
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        response.encoding = 'utf-8'
        # cd_data = json.loads(response.text)
        return json.loads(response.text)

        # items = data.get('StanReginCd', {}).get('row', [])
        # if items:
        #     return items[0].get('lawd_cd')  # 첫 번째 항목의 법정동 코드 반환
        # else:
        #     return None
    # else:
    #     print(f"Error fetching lawd_cd: {response.status_code}")
    #     return None
