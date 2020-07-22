import os
import json
from flask import Flask
from flask import request
from flask_api import status as api_status
from constants import COVID_API
import requests
from flask_redis import FlaskRedis
from flask_crontab import Crontab


app = Flask(__name__)
redis_client = FlaskRedis(app)
crontab = Crontab(app)

# app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/', methods=['GET'])
def home():
    return 'Hello, Corona Bot Developers!'


@crontab.job(minute="1", hour="0")
def parse_state_data():
    data = {}
    response = requests.request("GET", COVID_API, headers={}, data={})
    if response.status_code == 200:
        data = response.json()
        for key, value in data.items():
            data[key] = value
            district_data = data[key]['districtData']
            total_active, total_confirmed, total_deceased = 0, 0, 0
            for district_key, district_value in district_data.items():
                total_active += district_value['active']
                total_confirmed += district_value['confirmed']
                total_deceased += district_value['deceased']
            data[key]['total'] = {
                'active': total_active,
                'confirmed': total_confirmed,
                'deceased': total_deceased,
            }
            redis_client.set(key, str(data[key]))
    return data


@app.route('/covid', methods=['GET'])
def fetch_covid_api():
    final_data = parse_state_data()
    return final_data


if __name__ == '__main__':
    app.run()