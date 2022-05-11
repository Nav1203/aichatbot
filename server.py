import flask
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import pickle
from flask import request
import json
import pyttsx3
app=flask.Flask(__name__)
model = keras.models.load_model('chat_model')
with open("intents.json") as file:
    data = json.load(file)
    # load tokenizer object
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

    # load label encoder object
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)
    # parameters
max_len = 20
@app.route('/',methods=['POST'])
def recmsg_send():
    inp=request.form['msg']
    print("file=",inp)
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])
    for i in data['intents']:
        if i['tag'] == tag:
            print(tag)
            text=np.random.choice(i['responses'])
            return text
if __name__=='__main__':
    app.run()