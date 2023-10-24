import config
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from PyDictionary import PyDictionary

logging.basicConfig(level=logging.INFO) # log
bot = Bot(token=config.TOKEN) # init aiogram
dp = Dispatcher(bot)
dictionary=PyDictionary()

# /start command
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("qq eq")

# /chat command
@dp.message_handler(commands=['chat'])
async def cmd_chat(message: types.Message):
    user_word = message.text.replace('/chat', '', 1).strip()

    # Split the user_word string into a list of words
    words = user_word.split()

    meanings = {}

    for word in words:
        # Remove parentheses
        word = word.lstrip('(')
        # Fetch meanings for the word
        meanings[word] = dictionary.meaning(word)

    # Send the meanings back to the user
    response = ""
    for word, meaning in meanings.items():
        response += f'{word}:\n\n'
        for pos, definitions in meaning.items():
            response += f'Part of Speech: {pos}\n'
            for i, definition in enumerate(definitions, start=1):
                # Remove parentheses from the definition
                definition = definition.replace('(', '').replace(')', '')
                response += f'{i}. {definition}\n'
        response += '\n'

    await message.reply(response)

# print(dictionary.meaning("password"))

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)