
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
tf.keras.models.load_model("docs/z_bot")

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
        #print(intent['responses'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

#addDataOrig(data)

# Read text File
def read_text_file(file_path):
    dataT(file_path)

def dataT(file_path):
    text = textract.process(file_path)
    text = text.decode("utf-8")
    #text = text.split("\n\n");
    #print("text")
    #print(text)
    test = ''
    tag = ''
    sent = ''
    class Temp:
        def __init__(self, x):
            self.x = ""

    for i in text:
        if i != "?" and i != "." and i != "]" and i != "[" and i != "\n":
            test +=i
        if i == "]":
            tag = test
            test = ""
        if i == "?":
            #aux.append(y)
            sent = test
            sent = list(sent.split("?"))
            print(sent)
            test = ""
        if i == ".":
            #temp = Temp(test)
            #print("/n")
            temp = list(test.split("."))
            #print(temp)
            #print("/n")
            responses.append(temp)
            training_sentences.append(sent)
            training_labels.append(tag)
            if tag not in labels:
                print("#######################")
                labels.append(tag)
            entry = {'tag' : tag,'patterns' : sent, 'responses' : temp}
            data['intents'].append(entry)
            test = ""

# Change the directory
os.chdir(path)
# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".doc"):
        file_path = f"{os.getcwd()}/{file}"
        # call read text file function
        read_text_file(file_path)

print("data")
#print(data)
#for data in data['intents']:
print(data)
print("#")
#print("questions#######")
#print(training_sentences)
#print("training_labels#######")
#print(type(training_labels))
#print("training_labels#######")
#print(training_labels)
#print("responses######")
#print(type(responses))
#print("responses######")
#print(responses)
#print("labels#######")
#print(labels)

enc = LabelEncoder()
print("enc")
print(enc)
enc.fit(training_labels)
print("enc")
print(enc)
training_labels = enc.transform(training_labels)
print("training_labels")
print(training_labels)

vocab_size = 10000
embedding_dim = 16
max_len = 20
trunc_type = 'post'
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token) # adding out of vocabulary token
print("tokenizer")
print(tokenizer)
tokenizer.fit_on_texts(training_sentences)
print("tokenizer")
print(tokenizer)
word_index = tokenizer.word_index
print("word_index")
print(word_index)
sequences = tokenizer.texts_to_sequences(training_sentences)
print("sequences")
print(sequences)
padded = pad_sequences(sequences, truncating=trunc_type, maxlen=max_len)
print("padded")
print(padded)
classes = len(labels)
print("classes")
print(classes)
model = tf.keras.models.Sequential()
print("model.seque")
print(model)
model.add(keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_len))
print("model.embed")
print(model)
model.add(keras.layers.GlobalAveragePooling1D())
print("modelglobal")
print(model)
model.add(keras.layers.Dense(16, activation='relu'))
print("model.dense")
print(model)
model.add(keras.layers.Dense(16, activation='relu'))
print("modeldense")
print(model)
model.add(keras.layers.Dense(classes, activation='softmax'))
print("model.dense")
print(model)

model.summary()
print("model.sumary")
print(model)
training_labels_final = np.array(training_labels)
print("training_labels_final")
print(training_labels_final)
EPOCHS = 430
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print("model.compile")
print(model)
history = model.fit(padded, training_labels_final, epochs=EPOCHS)
print("history")
print(history)

# Get a respons for some unexpected input
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    result = model.predict(pad_sequences(tokenizer.texts_to_sequences([userText]),
                                         truncating=trunc_type, maxlen=max_len))
    print("arg")
    print(np.argmax(result))
    category = enc.inverse_transform([np.argmax(result)]) # labels[np.argmax(result)]
    print("result")
    print(result)
    print("categoria")
    print(category)
    #print("data")
    #print(data)
    #print("data intents")
    #print(data['intents'])
    for i in data['intents']:
        #print("i")
        #print(i)
        if i['tag']==category:
            print("i matched")
            print(i)
            print(i['responses'])
            return str(np.random.choice(i['responses']))

tf.keras.models.save_model(model, "z_bot")

if __name__ == "__main__":
    app.run()
