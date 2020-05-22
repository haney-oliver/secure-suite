import flask
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle as pkl
import tensorflow as tf
from flask_cors import CORS, cross_origin


print(tf.__version__)
app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model = load_model('../smss-malurl-model-nidl-1-relic.h5')
model.load_weights('../smss-malurl-nidl1-ne3-lr0.001-bs16-weights-00000003.h5')

tokenizer = Tokenizer()
with open('../tokenizer.pickle', 'rb') as tokenizer_file:
    tokenizer = pkl.load(tokenizer_file)


def tokenize(url):
    tokens = url.replace('?', ' ').replace('&', ' ').replace('+', ' ').replace('=', ' ').replace('://', ' ').replace('/', ' ').replace('-', ' ').replace('.',' ').replace('com', ' ').replace('www',' ').replace('https', ' ').replace('http', ' ')
    tokens = " ".join(tokens.split())
    return tokens


@app.route("/api/AnalyzeUrl", methods=["POST"])
@cross_origin()
def analyze_url():  
    data = flask.request.json
    response = {
        "status": 500,
        "urlGood": False,
        "tokens": "",
        "sequence": "",
        "errorMessage": ""
    }
    if (data == None):
        response["errorMessage"] = "Error: No URL recieved."
    else:
        url = data.get("url")
        print("Recieved url: {}".format(url))
        tokens = [tokenize(url)]
        print("URL tokens: {}".format(tokens[0]))
        seq = tokenizer.texts_to_sequences(np.array(tokens))
        response["tokens"] = tokens
        seq_to_save = [str(integer) for integer in seq[0]]
        response["sequence"] = ' '.join(seq_to_save)
        padded_seq = np.array(pad_sequences(seq, padding='post', maxlen=60))
        print("Seq: {}".format(seq[0]))
        prediction = model.predict(padded_seq)
        print("Prediction: {}".format(prediction))
        if (prediction < 0.5):
            response["urlGood"] = True
            response["status"] = 200
        elif (prediction > 0.5):
            response["urlGood"] = False
            response["status"] = 200
        else:
            response["urlGood"] = False
            response["errorMessage"] = "Error: Prediction not clear"
    return flask.jsonify(response)


app.run(host='0.0.0.0')
