# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers  import ChatterBotCorpusTrainer

chatbot = ChatBot('Jack')

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english.health")

while True:
    quest = input('Você: ')
    response = chatbot.get_response(quest)
    print('Bot: ',response)
