
import json
import nltk
import textract
import difflib
#handle multiple files https://www.geeksforgeeks.org/how-to-read-multiple-text-files-from-folder-in-python/
import os
nltk.download('stopwords')
nltk.download('punkt')
from flask import Flask, render_template, request
from nltk.corpus import stopwords
from nltk.tokenize  import word_tokenize
from chatterbot import ChatBot
from chatterbot.trainers  import ListTrainer
from difflib import SequenceMatcher
app = Flask(__name__)

path = "docs"
bot = ChatBot('Jacson')
#data = textract.process("test.txt", "utf-8")
#def open_file("test.doc")
#    file = open("test.doc", "r")
#    lines = file.read().getlines()
#    data1 = lines
#for i in data:
#    if i == "/n":
#        print(i)
#print(data)

trainer = ListTrainer(bot)
def dataT(file_path):
    text = textract.process(file_path)
    text = text.decode("utf-8")
    temp = []
    test = ''
    for i in text:
        if i != "\n":
            test +=i
        if i == "\n":
            temp.append(test)
        print(temp)
    return temp
# Change the directory
os.chdir(path)
# Read text File
def read_text_file(file_path):
    print(file_path)
    trainer.train(
        dataT(file_path)
    )

# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".doc"):
        file_path = f"{os.getcwd()}/{file}"
        # call read text file function
        read_text_file(file_path)


# Train the chat bot with a few responses
#trainer.train(
#    dataT()
#)

# Get a response for some unexpected input

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    response = bot.get_response(userText)
    print(response)
    return str(response)
if __name__ == "__main__":
    app.run()
