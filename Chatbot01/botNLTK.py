
import json
import textract
import difflib
import nltk

import requests

import re
import numpy as np
import tensorflow as tf
#handle multiple files https://www.geeksforgeeks.org/how-to-read-multiple-text-files-from-folder-in-python/
import os
from flask import Flask, render_template, request
from difflib import SequenceMatcher
#remove stopwords and punctuation
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
#print(" ".join(SnowballStemmer.languages))
from string import punctuation
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
app = Flask(__name__)

path = "docs"

badWords = set(stopwords.words('portuguese') + list(punctuation))
print(badWords)
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

addDataOrig(data)

# Read text File
def read_text_file(file_path):
    dataT(file_path)

def dataT(file_path):
    text = textract.process(file_path)
    text = text.decode("utf-8")
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
            #sent = list(sent.split("?"))
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


def compareW(userText, i):
    tokens = [word for word in nltk.word_tokenize(i) if word not in badWords]
    tokensUser = [word for word in nltk.word_tokenize(userText) if word not in badWords]
    print("REMOVENDO BAD CHAR E COMPARANDO")
    print(tokens)
    print(tokensUser)
    aux = ''
    aux2 = 0
    #print(type(tokensUser))
    size = len(tokens)
    sizeOK = 0
    #print("TOKEN USUÁRIO -> ",len(tokensUser))

    for j in tokens:
        for a in tokensUser:
            if a == j:
                sizeOK += 1
        #print("aux")
        #print(aux)

    if size != 0:
        if sizeOK >= size/1:
            print("TOKEN ATINGIU 100% DE COMPATIBILIDADE")
            return tokens
        if sizeOK >= size/1.25:
            print("TOKEN ATINGIU MAIS DE 75% DE COMPATIBILIDADE")
            return tokens
        if sizeOK >= size/1.5:
            print("TOKEN ATINGIU MAIS DE 66,6% DE COMPATIBILIDADE")
            return tokens
        if sizeOK >= size/2:
            print("TOKEN ATINGIU MAIS DE 50% DE COMPATIBILIDADE")
            return tokens
        sizeOK = 0

    print("nada")
    return "NoMatch"
    # Get a respons for some unexpected input
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    print(chr(27) + "[2J")
    result = ''

    for i in training_sentences:
        print(" ")
        print("QUESTÃO NO BANCO SENDO AVALIADA")
        print(i)
        aux = i
        result = compareW(userText.lower(), i.lower())
        #nltk.download()

        stem = SnowballStemmer('portuguese')
        #stemmer = nltk.stem("testando")
        #print(stemmer)

        if result != "NoMatch":
            for i in data['intents']:
                print("AVALIANDO RESULTADO VÁLIDO NESSES PATTERNS")
                print(i['patterns'])

                #print(stem.stem(userText))
                #print(stem.stem('correr')
                #print(stem.stem('')
                #print(stem.stem('')
                #print(stem.stem('')
                #print(stem.stem('')
                if isinstance(i['patterns'], str):
                    if aux == i['patterns']:
                        return str(np.random.choice(i['responses']))

                else:
                    for j in i['patterns']:
                        if aux == j:
                            return str(np.random.choice(i['responses']))
    if result == "NoMatch":

        # o resultado vai ser um Python dictionary, dai tu lê assim:
        #print('related_questions')
        #print(y['related_questions'][0]['answer'])
        #print(y['related_questions'][0]['source']['link'])
        #print(y['related_questions'][1]['answer'])
        #print(y['related_questions'][1]['source']['link'])
        #print(y['related_questions'][2]['answer'])
        #print(y['related_questions'][2]['source']['link'])

        def response():
            x = np.random.choice(3)
            print("XXXXX")
            print(x)
            print("XXXXX")
            params = {
                'api_key':'06B2D7373DE3482CB31C964CEFCA6CA0',
                'q': userText,
                'gl': 'br',
                'hl': 'pt-br',
                'sort_by': 'relevance',
                'time_period': 'last_year',
                'device': 'desktop',
                'output': 'json',
                'include_html': 'false'
            }

            # make the http GET request to Scale SERP
            api_result = requests.get('https://api.scaleserp.com/search', params)

            # print the JSON response from Scale SERP
            value = json.dumps(api_result.json())
            print(value)
            # dando parse no json:
            value = json.loads(value)
            try:
                print(value['knowledge_graph']['description'])
                value = value['knowledge_graph']['description'] + "<br> Fonte <br> " + value['knowledge_graph']['source']['link']
                return value
            except:
                try:
                    print("related_questions")
                    print(value['related_questions'][x]['answer'])
                    value = value['related_questions'][x]['answer'] + "<br> Fonte <br> " + value['related_questions'][x]['source']['link']
                    return value
                except:
                    print("organic_results")
                    print(value['organic_results'][x]['snippet'])
                    value = value['organic_results'][x]['snippet'] + "<br> Fonte <br> " + value['organic_results'][x]['link']
                    return value

        try:
            value = response()
            print(value)
            return str(value)
        except:
            for i in data['intents']:
                if i['tag'] == 'unknown':
                    return str(np.random.choice(i['responses']))

if __name__ == "__main__":
    app.run()
