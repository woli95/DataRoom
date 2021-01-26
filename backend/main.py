from flask import Flask
from flask_cors import CORS
from google.cloud import storage
import psycopg2


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
storage_client = storage.Client.from_service_account_json('DataRoom-b5e20df0599f.json')
import routes


if __name__ == "__main__":
    app.run()
