import json 
import numpy as np 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle

with open('intents.json') as file:
    data=json.load(file)
tsent,tlbl,lbl,res=[],[],[],[]

for intent in data['intents']:
    for pattern in intent['patterns']:
        tsent.append(pattern)
        tlbl.append(intent['tag'])
    res.append(intent['responses'])

    if intent['tag'] not in lbl:
        lbl.append(intent['tag'])

classn=len(lbl)
lblenc=LabelEncoder()
tlbl=lblenc.fit_transform(tlbl)

tkizer=Tokenizer(num_words=1000,oov_token='<OOV>',)
tkizer.fit_on_texts(tsent)
wrdind=tkizer.word_index
seq=tkizer.texts_to_sequences(tsent)
padseq=pad_sequences(seq,truncating='post',maxlen=20)

model=Sequential()
model.add(Embedding(1000,16,input_length=20))
model.add(GlobalAveragePooling1D())
model.add(Dense(16,activation='relu'))
model.add(Dense(16,activation='relu'))
model.add(Dense(classn,activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
model.summary()

his=model.fit(padseq,np.array(tlbl),epochs=500)
model.save("chat_model")

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tkizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
with open('label_encoder.pickle', 'wb') as ecn_file:
    pickle.dump(lblenc, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)