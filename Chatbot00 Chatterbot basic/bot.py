# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot('Jack')

trainer = ListTrainer(bot)

conv = ['oi', 'olá', 'olá, bom dia']

trainer.train(conv)

while True:
	quest = input('Você: ')

	response = bot.get_response(quest)

	print('Bot:', response)
