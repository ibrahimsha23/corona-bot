import os
import json
from flask import Flask
from flask import request
from flask_api import status as api_status


app = Flask(__name__)

# app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/', methods=['GET'])
def home():
    return 'Hello, Corona Bot Developers!'

if __name__ == '__main__':
    app.run()