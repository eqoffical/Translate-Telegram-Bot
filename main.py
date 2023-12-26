import config
import emoji
import random
import re
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from PyDictionary import PyDictionary
from deep_translator import GoogleTranslator

cldr_emoji_name = list(emoji.EMOJI_DATA.keys()) 
logging.basicConfig(level=logging.INFO) # log
bot = Bot(token=config.TOKEN) # init aiogram
dp = Dispatcher(bot)
dictionary = PyDictionary()
translator = GoogleTranslator(source='en', target='uk')
pattern = r"\([^()]*\)"

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

# global language state
pick_langauge = 0

# /lang
@dp.message_handler(commands=['lang'])
async def cmd_start(message: types.Message):

    global pick_langauge

    # language toggle
    pick_language_english = 0
    pick_langauge_ukrainian = 1

    if pick_langauge == pick_language_english:
        pick_langauge = pick_langauge_ukrainian
        await message.reply(f"{pick_langauge} 🇺🇦 Language was changed to ukrainian")

    elif pick_langauge == pick_langauge_ukrainian:
        pick_langauge = pick_language_english
        await message.reply(f"{pick_langauge} 🇺🇸 Language was changed to english")

    else:
        await message.reply(f"{pick_langauge} I dunno bruh")

# chatting
@dp.message_handler()
async def cmd_chat(message: types.Message):

    await message.answer("Thinking. . .")
    
    user_word = message.text

    try:
        words = user_word.split()
        meanings = {}

        try:
            for word in words:
                meanings[word] = dictionary.meaning(word)

            response = ""

            for word, meaning in meanings.items():

                pick_emoji = random.choice(cldr_emoji_name)
                translation = translator.translate(word)
                response = f"{emoji.emojize(pick_emoji)} Your word is: {word} ({translation})\n"

                for pos, definitions in meaning.items():
                    response += f'\n{pos}\n'

                    for i, definition in enumerate(definitions, start=1):
                        definition = definition.replace('(', '').replace(')', '')
                        response += f'{i}. {definition}\n'

                response += '\n'

            await message.reply(response)

        except: 
            translation = translator.translate(word)
            translation = re.sub(pattern, "", translation)
            await message.reply(f"❓ Your word is: {word}\nMaybe that's the translation: \"{translation}\"\nAnd I have no idea what is it, sorry")

    except:
        await message.reply(f"❌ There is no word\n"
                            "Type /help if you need some insctrutions")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
