from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential, Model
from keras.layers import Flatten, Dense, Embedding, GlobalMaxPool1D, Dropout, LSTM, Input, Conv1D, MaxPooling1D, concatenate
from keras.optimizers import adam
from keras.preprocessing.text import Tokenizer
from keras.utils import plot_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import pickle as pkl
import re


# Tunable hyperparameters
_nidl = [1, 2, 3]
_ne = [3, 6, 9]
_lr = [0.001, 0.005, 0.01]
_bs = [16, 32, 64]


def tokenize(url):
    tokens = url.replace('http', '').replace('https', '').replace('?', ' ').replace('&', ' ').replace('+', ' ').replace(
        '=', ' ').replace('://', ' ').replace('/', ' ').replace('-', ' ').replace('.', ' ').replace('com', ' ').replace('www', ' ')
    tokens = " ".join(tokens.split())
    return tokens


print("Loading Data...")
data = np.array(pd.DataFrame(
    pd.read_csv((Path("data/") / "data.csv"), ',', error_bad_lines=False))
    .sample(frac=1).reset_index(drop=True))

# One hot encoding to convert to decimal later
y = np.array([1 if row[1] == 'bad' else 0 for row in data])

tokenizer = Tokenizer(
    num_words=1000000, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}\t')

tokens = [tokenize(row[0]) for row in data]
tokenizer.fit_on_texts(tokens)

# Save tokenizer object with pickle to persist index dict for app use
with open('tokenizer.pickle', 'wb') as tokenizer_file:
    pkl.dump(tokenizer, tokenizer_file)
sequences = tokenizer.texts_to_sequences(tokens)
df1 = pd.DataFrame(np.array(pad_sequences(
    sequences, padding='post', maxlen=60)))
vocab_size = len(tokenizer.word_index) + 1

le = LabelEncoder()
df2 = pd.DataFrame(pd.read_csv(
    Path("data/") / "struct_data.csv")).fillna('')
df2 = df2.apply(le.fit_transform)

print("df1 shape: {}".format(df1.shape))
print("df2 shape: {}".format(df2.shape))

X = pd.concat([df1, df2], axis=1)

url_bad_count = 0
url_good_count = 0

X_train, X_validate, y_train, y_validate = train_test_split(
    X, y, test_size=0.15, random_state=1000)

print("\nX_train shape: {}\nX_validate shape: {}\ny_train shape: {}\ny_validate shape: {}".format(
    X_train.shape, X_validate.shape, y_train.shape, y_validate.shape))

X1_train = X_train.iloc[:, 0:60]
X1_validate = X_validate.iloc[:, 0:60]

X2_train = X_train[['url', 'url_domain', 'url_suffix', 'whois_registrar',
                    'whois_server_domain', 'whois_server_org', 'whois_org', 'url_domain_ip']]
X2_validate = X_validate[['url', 'url_domain', 'url_suffix', 'whois_registrar',
                          'whois_server_domain', 'whois_server_org', 'whois_org', 'url_domain_ip']]


def generate_model(nidl):
    unstruct_input = Input(shape=(60,))
    struct_input = Input(shape=(8,))

    # For ingesting non-strcutured url data
    m1 = Embedding(input_dim=vocab_size, output_dim=40,
                   input_length=60)(unstruct_input)
    m1 = Dropout(0.2)(m1)
    m1 = Conv1D(32, 5, padding='valid', activation='relu', strides=1)(m1)
    m1 = Dropout(0.2)(m1)
    m1 = MaxPooling1D()(m1)
    m1 = LSTM(40, dropout=0.2, recurrent_dropout=0.2)(m1)
    print("Shape of m1: {}".format(m1.shape))

    # For ingesting structured data
    m2 = Dense(32, activation='relu')(struct_input)
    m2 = Dropout(0.2)(m2)
    concat = concatenate([m1, m2])
    m = Dense(48)(concat)

    if(nidl == 1):
        m = Dense(20, activation='relu')(m)
        m = Dropout(0.2)(m)
    elif(nidl == 2):
        m = Dense(30, activation='relu')(m)
        m = Dropout(0.2)(m)
        m = Dense(15, activation='relu')(m)
        m = Dropout(0.2)(m)
    elif(nidl == 3):
        m = Dense(30, activation='relu')(m)
        m = Dropout(0.2)(m)
        m = Dense(20, activation='relu')(m)
        m = Dropout(0.2)(m)
        m = Dense(10, activation='relu')(m)
        m = Dropout(0.2)(m)
    m = Dense(5, activation='relu')(m)
    m = Dense(1, activation='sigmoid')(m)
    model = Model(inputs=[unstruct_input, struct_input], outputs=m)
    model.save('smss-malurl-model-nidl-{}.h5'.format(nidl))
    plot_model(model, to_file='smss-malurl-model-nidl-{}.png'.format(nidl))
    return model


def fit_data_to_model(nidl, ne, lr, bs, X, Xv, X2, X2v, y, yv, model):
    model.compile(loss='binary_crossentropy',
                  optimizer=adam(learning_rate=lr),
                  metrics=['accuracy'])
    print("Model Compiled...")
    mc = ModelCheckpoint("smss-malurl-nidl{}-ne{}-lr{}-bs{}-weights-".format(nidl, ne, lr, bs)+"{epoch:08d}.h5",
                         monitor='val_accuracy', save_weights_only=True, period=1)
    print(X.shape, X2.shape)
    print(Xv.shape, X2v.shape)
    print(y.shape, yv.shape)
    model_history = model.fit([X, X2], y, batch_size=bs,
                              epochs=ne, validation_data=([Xv, X2v], yv),
                              verbose=1, callbacks=[mc])

    # Save history of each network configuration for later plotting
    with open('smss-nidl{}-ne{}-lr{}-bs{}-history.pickle'.format(nidl, ne, lr, bs), 'wb') as history_file:
        pkl.dump(model_history.history, history_file)

    # Plot training & validation accuracy values
    plt.plot(model_history.history['accuracy'])
    plt.plot(model_history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')

    plt.show(block=False)

    plt.savefig("smss-acc-nidl{}-ne{}-lr{}-bs{}.png".format(nidl, ne, lr, bs))
    plt.clf()

    # Plot training & validation loss values
    plt.plot(model_history.history['loss'])
    plt.plot(model_history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')

    plt.show(block=False)

    plt.savefig("smss-loss-nidl{}-ne{}-lr{}-bs{}.png".format(nidl, ne, lr, bs))
    plt.clf()


# Perform training hyperparameter optimization
for nidl in _nidl:
    for ne in _ne:
        for lr in _lr:
            for bs in _bs:
                fit_data_to_model(nidl, ne, lr, bs, X1_train, X1_validate, X2_train, X2_validate,
                                  y_train, y_validate, generate_model(nidl))
