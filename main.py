# hint for developer 💡 print(dictionary.meaning("word"))

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

    words = user_word.split()
    meanings = {}

    try:

        for word in words:

            word = word.lstrip('(')
            meanings[word] = dictionary.meaning(word)

        response = ""
        for word, meaning in meanings.items():

            response += f'🔮 Your word is: {word}\n'

            for pos, definitions in meaning.items():

                response += f'\n{pos}\n'

                for i, definition in enumerate(definitions, start=1):

                    definition = definition.replace('(', '').replace(')', '')
                    response += f'{i}. {definition}\n'

            response += '\n'

        await message.reply(response)

    except:

        await message.reply(f'❌ Your word is: {word}\n\nAnd I have no idea what is it, sorry')

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)