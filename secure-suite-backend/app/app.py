import flask
import os
import json
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from app.api.api import api


app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/api/AnalyzeUrl", methods=["POST"])
@cross_origin()
def analyze_url():
    return api.create_and_or_analyze_url(flask.request)


@app.route("/api/GetUrl", methods=["POST"])
@cross_origin()
def get_url():
    return flask.jsonify(api.get_url(flask.request))


@app.route("/api/UpdateUrl", methods=["POST"])
@cross_origin()
def update_url():
    return flask.jsonify(api.update_url(flask.request))


@app.route("/api/RegisterUser", methods=["POST"])
@cross_origin()
def register_user():
    return flask.jsonify(api.register_user(flask.request))


@app.route("/api/LoginUser", methods=["POST"])
@cross_origin()
def login_user():
    return flask.jsonify(api.login_user(flask.request))


@app.route("/api/UpdateUser", methods=["POST"])
@cross_origin()
def update_user():
    return flask.jsonify(api.update_user(flask.request))


@app.route("/api/DeleteUser", methods=["POST"])
@cross_origin()
def delete_user():
    return flask.jsonify(api.delete_user(flask.request))


@app.route("/api/UpdateSession", methods=["POST"])
@cross_origin()
def update_session():
    return flask.jsonify(api.update_session(flask.request))


@app.route("/api/DeleteSession", methods=["POST"])
@cross_origin()
def delete_session():
    return flask.jsonify(api.delete_session(flask.request))


@app.route("/api/CreatePassword", methods=["POST"])
@cross_origin()
def create_password():
    return flask.jsonify(api.create_password(flask.request))


@app.route("/api/UpdatePassword", methods=["POST"])
@cross_origin()
def update_password():
    return flask.jsonify(api.update_password(flask.request))


@app.route("/api/ListPasswords", methods=["POST"])
@cross_origin()
def list_passwords():
    return flask.jsonify(api.list_passwords(flask.request))


@app.route("/api/DeletePassword", methods=["POST"])
@cross_origin()
def delete_password():
    return flask.jsonify(api.delete_password(flask.request))


@app.route("/api/GetPassword", methods=["POST"])
@cross_origin()
def get_password():
    return flask.jsonify(api.get_password(flask.request))


app.run(host='0.0.0.0')
