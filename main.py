# hint for developer 💡 print(dictionary.meaning("word"))

import config
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from PyDictionary import PyDictionary
from deep_translator import GoogleTranslator

logging.basicConfig(level=logging.INFO) # log
bot = Bot(token=config.TOKEN) # init aiogram
dp = Dispatcher(bot)
dictionary=PyDictionary()
translator = GoogleTranslator(source='en', target='uk')

# /start command
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user = message.from_user
    first_name = user.first_name
    await message.answer(f"Hello {first_name} 👋\n"
                        "\nI am a bot that will help you get the definition of any word!\n"
                        "\nType /help if you need some insctrutions\n"
			            "\n🐞 If you have any issues please report them")

# /help command
@dp.message_handler(commands=['help'])
async def cmd_start(message: types.Message):
    user = message.from_user
    first_name = user.first_name
    await message.reply(f"/chat \"word\" - put any word to get definitions (without quotation marks)\n"
                        "\n/translate \"слово\" - введіть будь-яке слово, щоб отримати визначення (без лапок)\n"
                        "\n/source - gives links to GitHub repository and the developer of the bot\n"
                        "\n🐞 If you have any issues please report them\n"
                        "\n/help - shows this message")

# /source code
@dp.message_handler(commands=['source'])
async def cmd_start(message: types.Message):
    link = "https://github.com/eqoffical/Translate-Telegram-Bot"
    await message.answer("Repository: <a href='{}'>GitHub</a>\n"
                        "Developer: @eqoffical".format(link), parse_mode=types.ParseMode.HTML)

# /chat command
@dp.message_handler(commands=['chat'])
async def cmd_chat(message: types.Message):

    await message.answer("Thinking. . .")
    
    user_word = message.text.replace('/chat', '', 1).strip()

    try:

        words = user_word.split()
        meanings = {}

        try:

            for word in words:

                word = word.lstrip('(')
                meanings[word] = dictionary.meaning(word)

            response = ""
            for word, meaning in meanings.items():

                translation = translator.translate(word)

                response += f"🔮 Your word is: {word} ({translation})\n"

                for pos, definitions in meaning.items():

                    response += f'\n{pos}\n'

                    for i, definition in enumerate(definitions, start=1):

                        definition = definition.replace('(', '').replace(')', '')
                        response += f'{i}. {definition}\n'

                response += '\n'

            await message.reply(response)

        except:

            await message.reply(f"❌ Your word is: {word}\nAnd I have no idea what is it, sorry")

    except:

        await message.reply(f"❌ There is no word\n"
                            "Type /help if you need some insctrutions")

# /translate command
@dp.message_handler(commands=['translate'])
async def cmd_chat(message: types.Message):

    await message.answer("Думаю. . .")

    user_word = message.text.replace('/translate', '', 1).strip()

    try:

        words = user_word.split()
        meanings = {}

        try:

            for word in words:

                word = word.lstrip('(')
                meanings[word] = dictionary.meaning(word)

            response = ""
            for word, meaning in meanings.items():

                translation = translator.translate(word)

                response += f"🔮 Ваше слово: {word} ({translation})\n"

                for pos, definitions in meaning.items():

                    translated_pos = translator.translate(pos)
                    response += f'\n{translated_pos}\n'

                    for i, definition in enumerate(definitions, start=1):

                        definition = definition.replace('(', '').replace(')', '')
                        translated_definition = translator.translate(definition)
                        response += f'{i}. {translated_definition}\n'

                response += '\n'

            await message.reply(response)

        except:

            await message.reply(f"❌ Ваше слово: {word}\nІ я навіть не знаю, що це таке, вибачте")

    except:

        await message.reply(f"❌ Тут немає слова\n"
                            "Спробуйте /help щоб отримати інструкції")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
