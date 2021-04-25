
import json
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
app = Flask(__name__)

with open('intents.json') as file:
    data = json.load(file)

from sklearn.preprocessing import LabelEncoder

training_sentences = []
training_labels = []
labels = []
responses = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])

    if intent['tag'] not in labels:
        labels.append(intent['tag'])

enc = LabelEncoder()
enc.fit(training_labels)
training_labels = enc.transform(training_labels)

vocab_size = 10000
embedding_dim = 16
max_len = 20
trunc_type = 'post'
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token) # adding out of vocabulary token
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, truncating=trunc_type, maxlen=max_len)

classes = len(labels)

model = tf.keras.models.Sequential()
model.add(keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation='relu'))
model.add(keras.layers.Dense(16, activation='relu'))
model.add(keras.layers.Dense(classes, activation='softmax'))

model.summary()
training_labels_final = np.array(training_labels)
EPOCHS = 500
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=EPOCHS)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    result = model.predict(pad_sequences(tokenizer.texts_to_sequences([userText]),
                                         truncating=trunc_type, maxlen=max_len))
    category = enc.inverse_transform([np.argmax(result)]) # labels[np.argmax(result)]
    for i in data['intents']:
        print(i)
        if i['tag']==category:
            return str(np.random.choice(i['responses']))

    tf.keras.models.save_model(model, "z_bot")

if __name__ == "__main__":
    app.run()
