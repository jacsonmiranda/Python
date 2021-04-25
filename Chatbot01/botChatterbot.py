
import json
import numpy as np
import tensorflow as tf
import nltk
import textract
import difflib
nltk.download('stopwords')
nltk.download('punkt')
from flask import Flask, render_template, request
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from nltk.tokenize  import word_tokenize
from chatterbot import ChatBot
from chatterbot.trainers  import ListTrainer
from difflib import SequenceMatcher
app = Flask(__name__)

bot = ChatBot('Jacson')
data = textract.process("test.txt", "utf-8")
#def open_file("test.doc")
#    file = open("test.doc", "r")
#    lines = file.read().getlines()
#    data1 = lines
for i in data:
    if i == "/n":
        print(i)
print(data)

trainer = ListTrainer(bot)

# Train the chat bot with a few responses
#trainer.train(data)

# Get a response for some unexpected input

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    response = bot.get_response(userText)
    return str(response)
if __name__ == "__main__":
    app.run()
