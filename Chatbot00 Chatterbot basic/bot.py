# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot('Jack',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'goodd',
            'output_text': 'ok '
        }
    ]
)

trainer = ListTrainer(bot)

conv = ['oi', 'olá']

trainer.train(conv)

while True:
	quest = input('Você: ')

	response = bot.get_response(quest)

	print('Bot:', response)
