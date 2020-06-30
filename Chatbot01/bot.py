# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers  import ChatterBotCorpusTrainer
chatterbot.response_selection.get_most_frequent_response(input_statement, response_list, storage=None)

chatbot = ChatBot('Jack')

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english.health")

while True:
    quest = input('Você: ')
    response = chatbot.get_response(quest)
    if(quest == "dying")
    print('Bot: ',response)

see this

https://chatterbot.readthedocs.io/en/stable/logic/index.html
