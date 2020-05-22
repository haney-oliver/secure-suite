from keras.preprocessing.text import Tokenizer
import pickle as pkl
import tensorflow as tf

tokenizer = Tokenizer()
with open('../tokenizer.pickle', 'rb') as tokenizer_file:
    tokenizer = pkl.load(tokenizer_file)


def tokenize(url):
    tokens = url.replace('?', ' ').replace('&', ' ').replace('+', ' ').replace('=', ' ').replace('://', ' ').replace(
        '/', ' ').replace('-', ' ').replace('.', ' ').replace('com', ' ').replace('www', ' ').replace('https', ' ').replace('http', ' ')
    tokens = " ".join(tokens.split())
    return tokens
