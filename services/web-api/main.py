from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db
from models.schemas import ma
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)


@app.route('/test', methods=['GET'])
def test():
    output = {"msg": "I'm the test endpoint."}
    return jsonify(output)


@app.route('/')
def index():
    return jsonify(ok='OK')
