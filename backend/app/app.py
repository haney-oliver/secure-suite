from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from tensorflow.keras.models import load_model
from tokenizer import tokenize, tokenizer
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
from datetime import datetime
import numpy as np
import uuid
import flask
import os
import hashlib
import json
import secrets
import string
import requests
import http.client
import re
import logging



app = flask.Flask(__name__) 
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.secret_key = os.environ.get('SECRET_KEY') 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.create_all()

# model
class User(db.Model):
    __tablename__ = 'user'
    user_key = db.Column(db.String(36), primary_key=True,
                         nullable=False, unique=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    user_email = db.Column(db.String(50), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    user_salt = db.Column(db.String(255), nullable=False)

    def __init__(self, user_key, user_name, user_email, user_password, user_salt):
        self.user_key = user_key
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.user_salt = user_salt

    @property
    def serialize(self):
        return {
            "user_key": self.user_key,
            "user_name": self.user_name,
            "user_email": self.user_email
        }


class Session(db.Model):
    __tablename__ = 'session'
    session_key = db.Column(
        db.String(36), primary_key=True, nullable=False, unique=True)
    ref_user_key = db.Column(
        db.String(36), unique=False)
    locked_out = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, session_key, ref_user_key):
        self.session_key = session_key
        self.ref_user_key = ref_user_key

    @property
    def serialize(self):
        return {
            "session_key": self.session_key,
            "ref_user_key": self.ref_user_key
        }


class Category(db.Model):
    __tablename__ = 'category'
    category_key = db.Column(
        db.String(36), primary_key=True, nullable=False, unique=True)
    ref_user_key = db.Column(db.String(36), db.ForeignKey('user.user_key'))
    category_name = db.Column(db.String(255), nullable=False)
    category_description = db.Column(db.Text, nullable=False)

    def __init__(self, category_key, ref_user_key, category_name, category_description):
        self.category_key = category_key
        self.ref_user_key = ref_user_key
        self.category_name = category_name
        self.category_description = category_description

    @property
    def serialize(self):
        return {
            "category_key": self.category_key,
            "category_name": self.category_name,
            "category_description": self.category_description
        }


class Url(db.Model):
    __tablename__ = 'url'
    url_key = db.Column(db.String(36), primary_key=True,
                        nullable=False, unique=True)
    ref_user_key = db.Column(db.String(36), db.ForeignKey('user.user_key'))
    url_string = db.Column(db.Text, nullable=False)
    url_tokens = db.Column(db.Text, nullable=False)
    url_sequence = db.Column(db.Text, nullable=False)
    url_good = db.Column(db.Boolean, nullable=False)

    def __init__(self, url_key, ref_user_key, url_string, url_tokens, url_sequence, url_good):
        self.url_key = url_key
        self.ref_user_key = ref_user_key
        self.url_string = url_string
        self.url_tokens = url_tokens
        self.url_sequence = url_sequence
        self.url_good = url_good

    @property
    def serialize(self):
        return {
            "url_key": self.url_key,
            "url_string": self.url_string,
            "url_good": self.url_good
        }


class Password(db.Model):
    __tablename__ = 'password'
    password_key = db.Column(
        db.String(36), primary_key=True, nullable=False, unique=True)
    ref_user_key = db.Column(db.String(36), db.ForeignKey(
        'user.user_key'), nullable=False)
    ref_category_key = db.Column(
        db.String(36), db.ForeignKey('category.category_key'), nullable=False)
    password_content = db.Column(db.String(50), nullable=False)
    password_username = db.Column(db.Text, nullable=False)
    password_url = db.Column(db.Text, nullable=False)

    def __init__(self, password_key, ref_user_key, ref_category_key, password_content, password_username, password_url):
        self.password_key = password_key
        self.ref_user_key = ref_user_key
        self.ref_category_key = ref_category_key
        self.password_content = password_content
        self.password_username = password_username
        self.password_url = password_url

    @property
    def serialize(self):
        return {
            "password_key": self.password_key,
            "password_username": self.password_username,
            "password_url": self.password_url,
            "password_content": self.password_content,
            "ref_category_key": self.ref_category_key
        }


# API
model = load_model('mal-url-net/model/smss-malurl-model-nidl-1-relic.h5')
model.load_weights(
    'mal-url-net/model/smss-malurl-nidl1-ne3-lr0.001-bs16-weights-00000003.h5')


SUCCESS_STATUS = 200
SUCCESS_MESSAGE_DEFAULT = "Success"

CREATE_SUCCESS_STATUS = 201
CREATE_SUCCESS_MESSAGE = "Successfully created resource"


SERVER_ERROR_STATUS = 500
SERVER_ERROR_MESSAGE_DEFAULT = "Something went wrong"

JSON_VALIDATION_ERROR_STATUS = 400
JSON_VALIDATION_ERROR_MESSAGE = "Unsupported POST data"

UNAUTHORIZED_ERROR_STATUS = 401
UNAUTHORIZED_ERROR_MESSAGE = "You need to be signed in to view this resource"

FORBIDDEN_ERROR_STATUS = 403
FORBIDDEN_ERROR_MESSAGE = "You lack the necessary permissions to view this resource"

NOT_FOUND_ERROR_CODE = 404
NOT_FOUND_ERROR_MESSAGE = "Resource not found"


# User auth
def validate_user_and_session(user_key, session_key):
    if user_key != None and session_key != None:
        user = User.query.get(user_key)
        session = Session.query.get(session_key)
        if (user != None and session !=None) and (user.user_key == session.ref_user_key and session.locked_out == False):
            return True
    return False


# Helpers
def calculate_url_analytics(urls):
    good_urls = []
    bad_urls = []
    for url in urls:
        if url.url_good:
            good_urls.append(url)
        else:
            bad_urls.append(url)
    return {
        "good_urls": [url.serialize for url in good_urls],
        "mal_urls": [url.serialize for url in bad_urls],
        "number_good_urls": len(good_urls),
        "number_mal_urls": len(bad_urls),
        "total_urls_visited": len(urls)
    }


def get_url_analysis(url, user_key):
    check = Url.query.filter_by(
        ref_user_key=user_key).filter_by(url_string=url).first()
    response = {}
    if (check == None):
        tokens = [tokenize(url)]
        seq = tokenizer.texts_to_sequences(np.array(tokens))
        padded_seq = np.array(pad_sequences(
            seq, padding='post', maxlen=60))
        prediction = model.predict(padded_seq)
        if (prediction < 0.5):
            response["url_good"] = True
            response["status"] = SUCCESS_STATUS
            response["message"] = SUCCESS_MESSAGE_DEFAULT
        elif (prediction > 0.5):
            response["url_good"] = False
            response["status"] = SUCCESS_STATUS
            response["message"] = SUCCESS_MESSAGE_DEFAULT
        else:
            response["status"] = SUCCESS_STATUS
            response["url_good"] = False
            response["message"] = "Error: Prediction not clear"
        create = Url(str(uuid.uuid4()), user_key, url, tokens[0], str(
            seq[0][0:]), response["url_good"])
        db.session.add(create)
        db.session.commit()
    else:
        response["status"] = SUCCESS_STATUS
        response["url_good"] = check.url_good
        response["message"] = "URL already visited by user"
    return response


# Url API
def expand_shortened_url_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    shortened_url = re.sub(
                        r'https?://', '', data["shortened_url"])
                    domain, path = shortened_url.split('/')
                    conn = http.client.HTTPConnection(domain)
                    conn.request('HEAD', '/'+path)
                    resp = conn.getresponse()
                    response["expanded_url"] = requests.get(
                        resp.getheader('location'), allow_redirects=True).url
                    analysis = get_url_analysis(
                        response["expanded_url"], data["user_key"])
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                    response["url_analysis"] = analysis
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def create_and_or_analyze_url_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            if validate_user_and_session(data["user_key"], data["session_key"]):
                url = data["url"]
                response = get_url_analysis(url, data["user_key"])
            else:
                response["status"] = UNAUTHORIZED_ERROR_STATUS
                response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def get_url_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    response["url"] = Url.query.get(
                        data["url_key"]).serialize
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def update_url_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    url = Url.query.get(data["url"]["url_key"])
                    url.url_good = data["url"]["url_good"]
                    db.session.commit()
                    response["url"] = {
                        "url_key": url.url_key,
                        "url_string": url.url_string,
                        "url_good": url.url_good
                    }
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def list_urls_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    urls = Url.query.filter_by(
                        ref_user_key=data["user_key"]).all()
                    response["urls"] = [url.serialize for url in urls]
                    response["analytics"] = calculate_url_analytics(urls)
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


# User API
def register_user_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                create = data["user"]
                salt = uuid.uuid4().hex
                hashed_password = hashlib.sha512(
                    (create["user_password"] + salt).encode('utf-8')).hexdigest()
                user = User(
                    str(uuid.uuid4()), create["user_name"], create["user_email"], hashed_password, salt)
                db.session.add(user)
                db.session.commit()
                response["user"] = {
                    "user_key": user.user_key,
                    "user_name": user.user_name,
                    "user_email": user.user_email
                }
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                logging.error(e)
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def login_user_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                user = User.query.filter_by(
                    user_name=data["user_name"]).first()
                if (user.user_password == hashlib.sha512((data["user_password"] + user.user_salt).encode('utf-8')).hexdigest()):
                    response["user"] = user.serialize
                    session = Session(str(uuid.uuid4()), user.user_key)
                    db.session.add(session)
                    db.session.commit()
                    response["session"] = session.serialize
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                else:
                    response["status"] = UNAUTHORIZED_ERROR_STATUS
                    response["message"] = "Invalid credentials. Try again."
            except Exception as e:
                logging.error(e)
                response["status"] = SERVER_ERROR_STATUS
                print(e)
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def logout_user_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    user = User.query.get(data["user_key"])
                    session = Session.query.get(data["session_key"])
                    if session.ref_user_key == user.user_key:
                        db.session.delete(session)
                        db.session.commit()
                        response["status"] = SUCCESS_STATUS
                        response["message"] = "User logged out."
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def update_user_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    user = User.query.get(data["user_key"])
                    user = data["user"]
                    response["user"] = user
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def delete_user_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    user = User.query.get(data["user_key"])
                    db.session.delete(user)
                    db.session.commit()
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


# Password API
def create_password_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    password = data["password"]
                    db.session.add(Password(str(uuid.uuid4()), password["ref_user_key"], password["ref_category_key"],
                                            password["password_content"], password["password_username"], password["password_url"]))
                    db.session.commit()
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def get_password_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    response["password"] = Password.query.get(data["password_key"]).serialize
                    print(response["password"])
                    response["status"] = CREATE_SUCCESS_STATUS
                    response["message"] = CREATE_SUCCESS_MESSAGE
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def update_password_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    update = data["password"]
                    print(update)
                    password = Password.query.get(data["password_key"])
                    password.password_content = update["password_content"]
                    password.ref_category_key = update["ref_category_key"]
                    password.password_username = update["password_username"]
                    password.password_url = update["password_url"]
                    db.session.commit()
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def list_passwords_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    response["passwords"] = [password.serialize for password in Password.query.filter_by(
                        ref_user_key=data["user_key"]).filter_by(ref_category_key=data["ref_category_key"]).all()]
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def delete_password_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    password = Password.query.get(data["password_key"])
                    db.session.delete(password)
                    db.session.commit()
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def generate_password_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if (data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    alphabet = string.ascii_letters
                    if data["include_numbers"]:
                        alphabet += "0123456789"
                    if data["include_symbols"]:
                        alphabet += "!@#$%^&*()<>?/,.:;'\"\\[{]}-_=+"                    
                    password = ''.join(secrets.choice(alphabet)
                                       for i in range(int(data["length"])))
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                    response["password"] = password
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


# Category API
def create_category_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if(data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    category = data["category"]
                    db.session.add(Category(str(uuid.uuid4()), category["ref_user_key"], category["category_name"], category["category_description"]))
                    db.session.commit()
                    response["status"] = CREATE_SUCCESS_STATUS
                    response["message"] = CREATE_SUCCESS_MESSAGE
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def update_category_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if(data == None):
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    update = data["category"]
                    category = Category.query.get(update.category_key)
                    category = update
                    db.session.commit()
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def get_category_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if data == None:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    print(data)
                    response["category"] = Category.query.get(
                        data["category_key"]).serialize
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def list_categories_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if data == None:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    response["categories"] = [category.serialize for category in Category.query.filter_by(
                        ref_user_key=data["user_key"]).all()]
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


def delete_category_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if validate_user_and_session(data["user_key"], data["session_key"]):
            if data == None:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
            else:
                try:
                    passwords = [password for password in Password.query.filter_by(
                        ref_user_key=data["user_key"]).filter_by(ref_category_key=data["category_key"]).all()]
                    for password in passwords:
                        db.session.delete(password)
                    db.session.delete(Category.query.get(data["category_key"]))
                    db.session.commit()
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                except Exception as e:
                    logging.error(e)
                    response["status"] = SERVER_ERROR_STATUS
                    response["message"] = str(e)
        else:
            response["status"] = UNAUTHORIZED_ERROR_STATUS
            response["message"] = UNAUTHORIZED_ERROR_MESSAGE
    return flask.Response(json.dumps(response), status=response["status"], mimetype="application/json")


# routes
@app.route("/api/ExpandShortenedUrl", methods=["POST"])
@cross_origin()
def expand_shortened_url():
    return expand_shortened_url_api(flask.request)


@app.route("/api/CreateOrAnalyzeUrl", methods=["POST"])
@cross_origin()
def analyze_url():
    return create_and_or_analyze_url_api(flask.request)


@app.route("/api/GetUrl", methods=["POST"])
@cross_origin()
def get_url():
    return get_url_api(flask.request)


@app.route("/api/ListUrls", methods=["POST"])
@cross_origin()
def list_urls():
    return list_urls_api(flask.request)


@app.route("/api/UpdateUrl", methods=["POST"])
@cross_origin()
def update_url():
    return update_url_api(flask.request)


@app.route("/api/RegisterUser", methods=["POST"])
@cross_origin()
def register_user():
    return register_user_api(flask.request)


@app.route("/api/LoginUser", methods=["POST"])
@cross_origin()
def login_user():
    return login_user_api(flask.request)


@app.route("/api/LogoutUser", methods=["POST"])
@cross_origin()
def logout_user():
    return logout_user_api(flask.request)


@app.route("/api/UpdateUser", methods=["POST"])
@cross_origin()
def update_user():
    return update_user_api(flask.request)


@app.route("/api/DeleteUser", methods=["POST"])
@cross_origin()
def delete_user():
    return delete_user_api(flask.request)


@app.route("/api/CreatePassword", methods=["POST"])
@cross_origin()
def create_password():
    return create_password_api(flask.request)


@app.route("/api/UpdatePassword", methods=["POST"])
@cross_origin()
def update_password():
    return update_password_api(flask.request)


@app.route("/api/ListPasswords", methods=["POST"])
@cross_origin()
def list_passwords():
    return list_passwords_api(flask.request)


@app.route("/api/DeletePassword", methods=["POST"])
@cross_origin()
def delete_password():
    return delete_password_api(flask.request)


@app.route("/api/GeneratePassword", methods=["POST"])
@cross_origin()
def generate_password():
    return generate_password_api(flask.request)


@app.route("/api/GetPassword", methods=["POST"])
@cross_origin()
def get_password():
    return get_password_api(flask.request)


@app.route("/api/CreateCategory", methods=["POST"])
@cross_origin()
def create_category():
    return create_category_api(flask.request)


@app.route("/api/UpdateCategory", methods=["POST"])
@cross_origin()
def update_category():
    return update_category_api(flask.request)


@app.route("/api/ListCategories", methods=["POST"])
@cross_origin()
def list_categories():
    return (list_categories_api(flask.request))


@app.route("/api/DeleteCategory", methods=["POST"])
@cross_origin()
def delete_category():
    return (delete_category_api(flask.request))


@app.route("/api/GetCategory", methods=["POST"])
@cross_origin()
def get_category():
    return (get_category_api(flask.request))


@app.route("/api/HealthCheck", methods=["GET"])
@cross_origin()
def health_check():
  return {"response": {"ok": True, "message": "App is running!", "status": 200}}

