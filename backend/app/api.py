from tensorflow.keras.models import load_model
from common.tokenizer import tokenize, tokenizer
from app.model import User, Url, Password
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import uuid


model = load_model('../smss-malurl-model-nidl-1-relic.h5')
model.load_weights(
    '../smss-malurl-nidl1-ne3-lr0.001-bs16-weights-00000003.h5')


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


class api:
    def __init__(self, db):
        self.db = db

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
                    response["user"] =
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
