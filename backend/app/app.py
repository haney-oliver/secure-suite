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
import hashlib


app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# model
class Role(db.Model):
    __tablename__ = 'role'
    role_key = db.Column(db.String(36), primary_key=True, nullable=False)
    role_name = db.Column(db.String(255), nullable=False)

    def __init__(self, role_key, role_name):
        self.role_key = role_key
        self.role_name = role_name


class Permission(db.Model):
    __tablename__ = 'permission'
    permission_key = db.Column(db.String(36), primary_key=True, nullable=False)
    ref_role_key = db.Column(db.String(36), db.ForeignKey('role.role_key'))
    permission_name = db.Column(db.String(255), nullable=False)

    def __init__(self, permission_key, ref_role_key, permission_name):
        self.permission_key = permission_key
        self.ref_role_key = ref_role_key
        self.permission_name = permission_name


class User(db.Model):
    __tablename__ = 'user'
    user_key = db.Column(db.String(36), primary_key=True, nullable=False)
    ref_role_key = db.Column(db.String(36), db.ForeignKey('role.role_key'))
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


# Url API
def create_and_or_analyze_url(request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            url = data["url"]
            check = Url.query.filter_by(url.url_sequence).first()
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
            else:
                 response["status"] = SUCCESS_STATUS
                 response["url_good"] = check.url_good
                 response["message"] = "URL already visited by user"
    return response


def get_url(request):
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


def update_url(request):
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


def list_urls(request):
    response = {}
    if request.is_json():
        data = request.json
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
def register_user(request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                create = data["user"]
                salt = uuid.uuid4().hex
                hashed_password = hashlib.sha512(create.user_password + salt).hexdigest()
                user = User(uuid.uuid4(), create.user_name, create.user_email, hashed_password, salt)
                db.session.add(user)
                db.session.commit()
                response["user"] = user
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def login_user(request):
    response = {}
    if request.is_json():
        data = request.json
        if (data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                user = User.query.filter_by(user_name=data["user_name"]).first()
                if (user.password == hashlib.sha512("user_password"+ user.salt).hexdigest()):
                    response["user"] = user
                    response["status"] = SUCCESS_STATUS
                    response["message"] = SUCCESS_MESSAGE_DEFAULT
                else:
                    response["status"] = SUCCESS_STATUS
                    response["message"] = "Invalid credentials. Try again."
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def update_user(request):
    response = {}
    if request.is_json():
        data = request.json
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


def delete_user(request):
    response = {}
    if request.is_json():
        data = request.json
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
def create_password(request):
    response = {}
    if request.is_json():
        data = request.json
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


def get_password(request):
    response = {}
    if request.is_json():
        data = request.json
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


def update_password(request):
    response = {}
    if request.is_json():
        data = request.json
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


def list_passwords(request):
    response = {}
    if request.is_json():
        data = request.json
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


def delete_password(request):
    response = {}
    if request.is_json():
        data = request.json
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
def create_role(request):
    response = {}
    if request.is_json():
        data = request.json
        if(data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                role = request["role"]
                db.session.add(Role(uuid.uuid4(), role.role_name))
                db.session.commit()
                response["status"] = CREATE_SUCCESS_STATUS
                response["message"] = CREATE_SUCCESS_MESSAGE
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def update_role(request):
    response = {}
    if request.is_json():
        data = request.json
        if(data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                update = data["role"]
                role = Role.query.get(update.role_key)
                role = update
                db.session.commit()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def get_role(request):
    response = {}
    if request.is_json():
        data = request.json
        if data == None:
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                response["role"] = Role.query.get(data["role_key"])
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)


def list_roles(request):
    response = {}
    if request.is_json():
        data = request.json
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


def delete_role(request):
    response = {}
    if request.is_json():
        data = request.json
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


# Permission API
def create_permission(request):
    response = {}
    if request.is_json():
        data = request.json
        if(data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                permission = request["permission"]
                db.session.add(Permission(uuid.uuid4(), permission.ref_role_key, permission.permission_name))
                db.session.commit()
                response["status"] = CREATE_SUCCESS_STATUS
                response["message"] = CREATE_SUCCESS_MESSAGE
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def update_permission(request):
    response = {}
    if request.is_json():
        data = request.json
        if(data == None):
            response["status"] = SERVER_ERROR_STATUS
            response["message"] = SERVER_ERROR_MESSAGE_DEFAULT
        else:
            try:
                update = data["permission"]
                permission = Permission.query.get(update.permission_key)
                permission = update
                db.session.commit()
                response["status"] = SUCCESS_STATUS
                response["message"] = SUCCESS_MESSAGE_DEFAULT
            except Exception as e:
                response["status"] = SERVER_ERROR_STATUS
                response["message"] = str(e)
    return response


def get_permission(request):
    response = {}
    if request.is_json():
        data = request.json
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


def list_permissions(request):
    response = {}
    if request.is_json():
        data = request.json
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


def delete_permission(request):
    response = {}
    if request.is_json():
        data = request.json
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


# Category API
def create_category(request):
    response = {}
    if request.is_json():
        data = request.json
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


def update_category(request):
    response = {}
    if request.is_json():
        data = request.json
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


def get_category(request):
    response = {}
    if request.is_json():
        data = request.json
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


def list_categories(request):
    response = {}
    if request.is_json():
        data = request.json
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


def delete_category(request):
    response = {}
    if request.is_json():
        data = request.json
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


@app.route("/api/CreateRole", methods=["POST"])
@cross_origin()
def create_role():
    return flask.jsonify(create_role(flask.request))


@app.route("/api/UpdateRole", methods=["POST"])
@cross_origin()
def update_role():
    return flask.jsonify(update_role(flask.request))


@app.route("/api/ListRoles", methods=["POST"])
@cross_origin()
def list_roles():
    return flask.jsonify(list_roles(flask.request))


@app.route("/api/DeleteRole", methods=["POST"])
@cross_origin()
def delete_role():
    return flask.jsonify(delete_role(flask.request))


@app.route("/api/GetRole", methods=["POST"])
@cross_origin()
def get_role():
    return flask.jsonify(get_role(flask.request))


@app.route("/api/CreatePermission", methods=["POST"])
@cross_origin()
def create_permission():
    return flask.jsonify(create_permission(flask.request))


@app.route("/api/UpdatePermission", methods=["POST"])
@cross_origin()
def update_permission():
    return flask.jsonify(update_permission(flask.request))


@app.route("/api/ListPermissions", methods=["POST"])
@cross_origin()
def list_permissions():
    return flask.jsonify(list_permissions(flask.request))


@app.route("/api/DeletePermission", methods=["POST"])
@cross_origin()
def delete_permission():
    return flask.jsonify(delete_permission(flask.request))


@app.route("/api/GetPermission", methods=["POST"])
@cross_origin()
def get_permission():
    return flask.jsonify(get_permission(flask.request))


@app.route("/api/CreateCategory", methods=["POST"])
@cross_origin()
def create_category():
    return flask.jsonify(create_category(flask.request))


@app.route("/api/UpdateCategory", methods=["POST"])
@cross_origin()
def update_category():
    return flask.jsonify(update_category(flask.request))


@app.route("/api/ListCategories", methods=["POST"])
@cross_origin()
def list_categories():
    return flask.jsonify(list_categories(flask.request))


@app.route("/api/DeleteCategory", methods=["POST"])
@cross_origin()
def delete_category():
    return flask.jsonify(delete_category(flask.request))


@app.route("/api/GetCategory", methods=["POST"])
@cross_origin()
def get_category():
    return flask.jsonify(get_category(flask.request))


app.run(host='0.0.0.0')
