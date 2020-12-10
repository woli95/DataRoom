from flask import Flask
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
import routes

if __name__ == "__main__":
    app.run()
