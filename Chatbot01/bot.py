# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers  import ListTrainer

bot = ChatBot(
    'Jacson',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'socorro',
            'output_text': 'seu caso eh urgente'
        }
    ]
)

trainer = ListTrainer(bot)

# Train the chat bot with a few responses
trainer.train([
    'oi',
    'bom dia'
])

# Get a response for some unexpected input
while True:
    quest = input('Voce: ')
    response = bot.get_response(quest)
    print(response)
