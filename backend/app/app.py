from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from tensorflow.keras.models import load_model
from tokenizer import tokenize, tokenizer
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import uuid
import flask
import os


app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.run(host='0.0.0.0')


# model
class User(db.Model):
    __tablename__ = 'user'
    user_key = db.Column(db.String(36), primary_key=True, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    user_salt = db.Column(db.String(50), nullable=False)

    def __init__(self, user_key, user_name, user_email, user_password, user_salt):
        self.user_key = user_key
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.user_salt = user_salt


class Category(db.Model):
    __tablename__ = 'category'
    category_key = db.Column(db.String(36), primary_key=True, nullable=False)
    ref_user_key = db.Column(db.String(36), db.ForeignKey('user.user_key'))
    category_name = db.Column(db.String(10), nullable=False)
    category_description = db.Column(db.Text, nullable=False)

    def __init__(self, category_key, ref_user_key, category_name, category_description):
        self.category_key = category_key
        self.ref_user_key = ref_user_key
        self.category_name = category_name
        self.category_description = category_description


class Url(db.Model):
    __tablename__ = 'url'
    url_key = db.Column(db.String(36), primary_key=True, nullable=False)
    ref_user_key = db.Column(db.String(36), db.ForeignKey('user.user_key'))
    url_tokens = db.Column(db.Text, nullable=False)
    url_sequence = db.Column(db.Text, nullable=False)
    url_good = db.Column(db.Boolean, nullable=False)

    def __init__(self, url_key, ref_user_key, url_tokens, url_sequence, url_good):
        self.url_key = url_key
        self.ref_user_key = ref_user_key
        self.url_tokens = url_tokens
        self.url_sequence = url_sequence
        self.url_good = url_good


class Password(db.Model):
    __tablename__ = 'password'
    password_key = db.Column(db.String(36), primary_key=True, nullable=False)
    ref_user_key = db.Column(db.String(36), db.ForeignKey(
        'user.user_key'), nullable=False)
    ref_category_key = db.Column(
        db.String(36), db.ForeignKey('category.category_key'), nullable=False)
    password_content = db.Column(db.String(50), nullable=False)
    password_username = db.Column(db.Text, nullable=False)
    password_url = db.Column(db.Text, nullable=False)

    def __init__(self, password_key, ref_user_key, ref_category_key, password_content, password_username, password_url, password_salt):
        self.password_key = password_key
        self.ref_user_key = ref_user_key
        self.ref_category_key = ref_category_key
        self.password_content = password_content
        self.password_username = password_username
        self.password_url = password_url
        self.password_salt = password_salt

# api
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


def create_and_or_analyze_url(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            url = data["url"]
            tokens = [tokenize(url)]
            seq = tokenizer.texts_to_sequences(np.array(tokens))
            response["tokens"] = tokens
            seq_to_save = [str(integer) for integer in seq[0]]
            response["sequence"] = ' '.join(seq_to_save)
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
    return response

def get_url(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def update_url(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                url = Url.query.get(data["url_key"])
                url.url_good = request["url_good"]
                db.session.commit()
                response["url"] = url
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def list_urls(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["urls"] = Url.query.filter_by(
                    Url.ref_user_key).all()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def register_user(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                create = data["user"]
                user = User(uuid.uuid4(), create.user_name, create.user_email, create.user_password, 'salt')
                response["user"] = user
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def login_user(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def update_user(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def delete_user(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def update_session(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def delete_session(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def create_password(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def get_password(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def update_password(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def list_passwords(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

def delete_password(self, request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["url"] = Url.query.get(data["url_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response

# routes
@app.route("/api/AnalyzeUrl", methods=["POST"])
@cross_origin()
def analyze_url():
    return create_and_or_analyze_url(flask.request)


@app.route("/api/GetUrl", methods=["POST"])
@cross_origin()
def get_url():
    return flask.jsonify(get_url(flask.request))


@app.route("/api/UpdateUrl", methods=["POST"])
@cross_origin()
def update_url():
    return flask.jsonify(update_url(flask.request))


@app.route("/api/RegisterUser", methods=["POST"])
@cross_origin()
def register_user():
    return flask.jsonify(register_user(flask.request))


@app.route("/api/LoginUser", methods=["POST"])
@cross_origin()
def login_user():
    return flask.jsonify(login_user(flask.request))


@app.route("/api/UpdateUser", methods=["POST"])
@cross_origin()
def update_user():
    return flask.jsonify(update_user(flask.request))


@app.route("/api/DeleteUser", methods=["POST"])
@cross_origin()
def delete_user():
    return flask.jsonify(delete_user(flask.request))


@app.route("/api/UpdateSession", methods=["POST"])
@cross_origin()
def update_session():
    return flask.jsonify(update_session(flask.request))


@app.route("/api/DeleteSession", methods=["POST"])
@cross_origin()
def delete_session():
    return flask.jsonify(delete_session(flask.request))


@app.route("/api/CreatePassword", methods=["POST"])
@cross_origin()
def create_password():
    return flask.jsonify(create_password(flask.request))


@app.route("/api/UpdatePassword", methods=["POST"])
@cross_origin()
def update_password():
    return flask.jsonify(update_password(flask.request))


@app.route("/api/ListPasswords", methods=["POST"])
@cross_origin()
def list_passwords():
    return flask.jsonify(list_passwords(flask.request))


@app.route("/api/DeletePassword", methods=["POST"])
@cross_origin()
def delete_password():
    return flask.jsonify(delete_password(flask.request))


@app.route("/api/GetPassword", methods=["POST"])
@cross_origin()
def get_password():
    return flask.jsonify(get_password(flask.request))
