
import json
import textract
import difflib
import numpy as np
import tensorflow as tf
#handle multiple files https://www.geeksforgeeks.org/how-to-read-multiple-text-files-from-folder-in-python/
import os
from flask import Flask, render_template, request
from difflib import SequenceMatcher
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
app = Flask(__name__)

path = "docs"

training_sentences = []
training_labels = []
labels = []
responses = []

with open('data.json') as file:
    data = json.load(file)

def addDataOrig(data):
    for intent in data['intents']:
        for pattern in intent['patterns']:
            training_sentences.append(pattern)
            training_labels.append(intent['tag'])
        responses.append(intent['responses'])
        print(intent['responses'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

addDataOrig(data)

def dataT(file_path):
    text = textract.process(file_path)
    text = text.decode("utf-8")
    test = ''
    class Temp:
        def __init__(self, x):
            self.x = ""

    for i in text:
        if i != "?" and i != "." and i != "]" and i != "\n":
            test +=i
        if i == "]":
            training_labels.append(test)
            labels.append(test)
            test = ""
        if i == "?":
            training_sentences.append(test)
            #aux.append(y)
            test = ""
        if i == ".":
            #temp = Temp(test)
            print("/n")
            temp = list(test.split("."))
            print(temp)
            print("/n")
            responses.append(temp)
            test = ""

# Change the directory
os.chdir(path)

# Read text File
def read_text_file(file_path):
    dataT(file_path)
# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".doc"):
        file_path = f"{os.getcwd()}/{file}"
        # call read text file function
        read_text_file(file_path)

print("questions#######")
print(training_sentences)
print("training_labels#######")
print(type(training_labels))
print("training_labels#######")
print(training_labels)
print("responses######")
print(type(responses))
print("responses######")
print(responses)
#print("labels#######")
#print(labels)

enc = LabelEncoder()
enc.fit(training_labels)
training_labels = enc.transform(training_labels)

vocab_size = 20000
embedding_dim = 26
max_len = 40
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
EPOCHS = 200
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=EPOCHS)

# Get a response for some unexpected input

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    result = model.predict(pad_sequences(tokenizer.texts_to_sequences([userText]),
                                         truncating=trunc_type, maxlen=max_len))
    category = enc.inverse_transform([np.argmax(result)]) # labels[np.argmax(result)]
    print(result)
    print(category)
    print(data)
    print(data['intents'])
    for i in data['intents']:
        if i['tag']==category:
            print(i)
            return str(np.random.choice(i['responses']))

    tf.keras.models.save_model(model, "z_bot")

if __name__ == "__main__":
    app.run()
