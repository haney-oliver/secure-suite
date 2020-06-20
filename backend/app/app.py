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


app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql://secure_suite:IWANTTOBEHACKED@localhost:3306/secure_suite')
app.secret_key = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# model
class User(db.Model):
    __tablename__ = 'user'
    user_key = db.Column(db.String(36), primary_key=True, nullable=False, unique=True)
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


class Session(db.Model):
    __tablename__ = 'session'
    session_key = db.Column(db.String(36), primary_key=True, nullable=False, unique=True)
    ref_user_key = db.Column(db.String(36), db.ForeignKey('user.user_key'), unique=True)
    time_create = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    time_update = db.Column(db.DateTime())
    locked_out = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, session_key, ref_user_key):
        self.session_key = session_key
        self.ref_user_key = ref_user_key


class Category(db.Model):
    __tablename__ = 'category'
    category_key = db.Column(db.String(36), primary_key=True, nullable=False, unique=True)
    ref_user_key = db.Column(db.String(36), db.ForeignKey('user.user_key'))
    category_name = db.Column(db.String(10), nullable=False, unique=True)
    category_description = db.Column(db.Text, nullable=False)

    def __init__(self, category_key, ref_user_key, category_name, category_description):
        self.category_key = category_key
        self.ref_user_key = ref_user_key
        self.category_name = category_name
        self.category_description = category_description


class Url(db.Model):
    __tablename__ = 'url'
    url_key = db.Column(db.String(36), primary_key=True, nullable=False, unique=True)
    ref_user_key = db.Column(db.String(36), db.ForeignKey('user.user_key'))
    url_string = db.Column(db.String(36), nullable=False, unique=True)
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


class Password(db.Model):
    __tablename__ = 'password'
    password_key = db.Column(db.String(36), primary_key=True, nullable=False, unique=True)
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
    user = User.query.get(user_key)
    session = Session.query.get(session_key)
    if (user.user_key == session.ref_user_key && session.locked_out == False):
        return True
    else:
        return False


# Url API
def create_and_or_analyze_url_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            url = data["url"]
            check = Url.query.filter_by(url_string=url).first()
            print(check)
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
                create = Url(uuid.uuid4(), data["ref_user_key"], url, tokens, seq, response["url_good"])
                db.session.add(create)
                db.session.commit()
            else:
                 response["status"] = SUCCESS_STATUS
                 response["url_good"] = check.url_good
                 response["message"] = "URL already visited by user"
    return response


def get_url_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
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


def update_url_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
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


def list_urls_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["urls"] = Url.query.filter_by(
                    ref_user_key=data["ref_user_key"]).all()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


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
                hashed_password = hashlib.sha512((create["user_password"] + salt).encode('utf-8')).hexdigest()
                user = User(uuid.uuid4(),create["user_name"], create["user_email"], hashed_password, salt)
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
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def login_user_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                user = User.query.filter_by(user_name=data["user_name"]).first()
                if (user.user_password == hashlib.sha512(("user_password"+ user.user_salt).encode('utf-8')).hexdigest()):
                    check_session = Session.query.filter_by(ref_user_key=user.user_key).first()
                    if check_session != None:
                        response["status"] = UNAUTHORIZED_ERROR_STATUS
                        response["message"] = "User already logged in."
                        return response
                    response["user"] = {
                        "user_key": user.user_key,
                        "ref_role_key": user.ref_role_key,
                        "user_name": user.user_name,
                        "user_email": user.user_email
                    }
                    session = Session(uuid.uuid4(), user.user_key)
                    db.session.add(session)
                    db.session.commit()
                    response["session"] = {
                        "session_key": session.session_key,
                        "ref_user_key": session.ref_user_key,
                        "time_create": session.time_create,
                        "time_update": session.time_update,
                        "locked_out": session.locked_out
                    }
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                else:
                    response["status"] = SUCCESS_STATUS
                    response["message"] = "Invalid credentials. Try again."
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def logout_user_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
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
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def update_user_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
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
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def delete_user_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
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
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


# Password API
def create_password_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                password = data["password"]
                db.session.add(Password(uuid.uuid4(), password.ref_user_key, password.ref_category_key, password.password_content, password.password_username, password.password_url))
                db.session.commit()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def get_password_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response[""] = Url.query.get(data["url_key"])
                response["status"] = CREATE_SUCCESS_STATUS
                response["message"] = CREATE_SUCCESS_MESSAGE
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def update_password_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                update = data["password"]
                password = Password.query.get(data["password_key"])
                password = update
                db.session.commit()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def list_passwords_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["passwords"] = Password.query.filter_by(ref_user_key=data["ref_user_key"]).all()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def delete_password_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                password = Password.query.get(data["password_key"])
                db.session.delete(password)
                db.session.commit
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


# Role API
def create_role_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if(data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                db.session.add(Role(uuid.uuid4(), data["role"]["role_name"]))
                db.session.commit()
                response["status"] = CREATE_SUCCESS_STATUS
                response["message"] = CREATE_SUCCESS_MESSAGE
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def update_role_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if(data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                role = Role.query.get(data["role"]["role_key"])
                role.role_name = data["role"]["role_name"]
                db.session.commit()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def get_role_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if data == None:
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                role = Role.query.get(data["role_key"])
                response["role"] = { "role_key": role.role_key, "role_name": role.role_name }
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def list_roles_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if data == None:
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["roles"] = Role.query.filter_by(ref_user_key=data["ref_user_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)


def delete_role_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if data == None:
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                db.session.delete(Role.query.get(data["role_key"]))
                db.session.commit()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


# Permission API
def create_permission_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if(data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                permission = data["permission"]
                db.session.add(Permission(uuid.uuid4(), permission["ref_role_key"], permission["permission_name"]))
                db.session.commit()
                response["status"] = CREATE_SUCCESS_STATUS
                response["message"] = CREATE_SUCCESS_MESSAGE
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def update_permission_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if(data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                update = data["permission"]
                permission = Permission.query.get(update["permission_key"])
                permission = update
                db.session.commit()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def get_permission_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if data == None:
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["permission"] = Permission.query.get(data["permission_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)


def list_permissions_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if data == None:
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["permissions"] = Permission.query.filter_by(ref_role_key=data["ref_role_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)


def delete_permission_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if data == None:
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                db.session.delete(Permission.query.get(data["permission_key"]))
                db.session.commit()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


# Category API
def create_category_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if(data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                category = request["role"]
                db.session.add(Category(uuid.uuid4(), category.ref_user_key, category.category_name, category.category_decription))
                db.session.commit()
                response["status"] = CREATE_SUCCESS_STATUS
                response["message"] = CREATE_SUCCESS_MESSAGE
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def update_category_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
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
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def get_category_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if data == None:
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["category"] = Category.query.get(data["category_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)


def list_categories_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if data == None:
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["categories"] = Category.query.filter_by(ref_user_key=data["ref_user_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)


def delete_category_api(request):
    response = {}
    if request.is_json:
        data = request.get_json()
        if data == None:
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                db.session.delete(Category.query.get(data["category_key"]))
                db.session.commit()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)


# routes
@app.route("/api/CreateOrAnalyzeUrl", methods=["POST"])
@cross_origin()
def analyze_url():
    return create_and_or_analyze_url_api(flask.request)


@app.route("/api/GetUrl", methods=["POST"])
@cross_origin()
def get_url():
    return flask.jsonify(get_url_api(flask.request))


@app.route("/api/UpdateUrl", methods=["POST"])
@cross_origin()
def update_url():
    return flask.jsonify(update_url_api(flask.request))


@app.route("/api/RegisterUser", methods=["POST"])
@cross_origin()
def register_user():
    return flask.jsonify(register_user_api(flask.request))


@app.route("/api/LoginUser", methods=["POST"])
@cross_origin()
def login_user():
    return flask.jsonify(login_user_api(flask.request))


@app.route("/api/LogoutUser", methods=["POST"])
@cross_origin()
def logout_user():
    return flask.jsonify(logout_user_api(flask.request))


@app.route("/api/UpdateUser", methods=["POST"])
@cross_origin()
def update_user():
    return flask.jsonify(update_user_api(flask.request))


@app.route("/api/DeleteUser", methods=["POST"])
@cross_origin()
def delete_user():
    return flask.jsonify(delete_user_api(flask.request))


@app.route("/api/CreatePassword", methods=["POST"])
@cross_origin()
def create_password():
    return flask.jsonify(create_password_api(flask.request))


@app.route("/api/UpdatePassword", methods=["POST"])
@cross_origin()
def update_password():
    return flask.jsonify(update_password_api(flask.request))


@app.route("/api/ListPasswords", methods=["POST"])
@cross_origin()
def list_passwords():
    return flask.jsonify(list_passwords_api(flask.request))


@app.route("/api/DeletePassword", methods=["POST"])
@cross_origin()
def delete_password():
    return flask.jsonify(delete_password_api(flask.request))


@app.route("/api/GetPassword", methods=["POST"])
@cross_origin()
def get_password():
    return flask.jsonify(get_password_api(flask.request))


@app.route("/api/CreateRole", methods=["POST"])
@cross_origin()
def create_role():
    return flask.jsonify(create_role_api(flask.request))


@app.route("/api/UpdateRole", methods=["POST"])
@cross_origin()
def update_role():
    return flask.jsonify(update_role_api(flask.request))


@app.route("/api/ListRoles", methods=["POST"])
@cross_origin()
def list_roles():
    return flask.jsonify(list_roles_api(flask.request))


@app.route("/api/DeleteRole", methods=["POST"])
@cross_origin()
def delete_role():
    return flask.jsonify(delete_role_api(flask.request))


@app.route("/api/GetRole", methods=["POST"])
@cross_origin()
def get_role():
    return flask.jsonify(get_role_api(flask.request))


@app.route("/api/CreatePermission", methods=["POST"])
@cross_origin()
def create_permission():
    return flask.jsonify(create_permission_api(flask.request))


@app.route("/api/UpdatePermission", methods=["POST"])
@cross_origin()
def update_permission():
    return flask.jsonify(update_permission_api(flask.request))


@app.route("/api/ListPermissions", methods=["POST"])
@cross_origin()
def list_permissions():
    return flask.jsonify(list_permissions_api(flask.request))


@app.route("/api/DeletePermission", methods=["POST"])
@cross_origin()
def delete_permission():
    return flask.jsonify(delete_permission_api(flask.request))


@app.route("/api/GetPermission", methods=["POST"])
@cross_origin()
def get_permission():
    return flask.jsonify(get_permission_api(flask.request))


@app.route("/api/CreateCategory", methods=["POST"])
@cross_origin()
def create_category():
    return flask.jsonify(create_category_api(flask.request))


@app.route("/api/UpdateCategory", methods=["POST"])
@cross_origin()
def update_category():
    return flask.jsonify(update_category_api(flask.request))


@app.route("/api/ListCategories", methods=["POST"])
@cross_origin()
def list_categories():
    return flask.jsonify(list_categories_api(flask.request))


@app.route("/api/DeleteCategory", methods=["POST"])
@cross_origin()
def delete_category():
    return flask.jsonify(delete_category_api(flask.request))


@app.route("/api/GetCategory", methods=["POST"])
@cross_origin()
def get_category():
    return flask.jsonify(get_category_api(flask.request))


app.run(host='0.0.0.0')
