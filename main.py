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
                        "I am a bot that will help you get the definition of any word!\n\n"
                        "Type /help if you need some insctrutions\n\n"
                        "🐞 If you have any issues please report them")

# /help command
@dp.message_handler(commands=['help'])
async def cmd_start(message: types.Message):
    user = message.from_user
    first_name = user.first_name
    await message.reply("To get the definition of any word, just type it in the chat\n"
                        "If there is more than one, it simply translates it\n\n"
                        "/help - shows this message\n"
                        "/source - gives links to GitHub and the developer of the bot\n\n"
                        "🐞 If you have any issues please report them")

# /source code
@dp.message_handler(commands=['source'])
async def cmd_start(message: types.Message):
    link = "https://github.com/eqoffical/Translate-Telegram-Bot"
    await message.answer("Repository: <a href='{}'>GitHub</a>\n"
                        "Developer: @eqoffical".format(link), parse_mode=types.ParseMode.HTML)

# chatting
@dp.message_handler()
async def cmd_chat(message: types.Message):
        
    total_words = 0
    text = message.text.replace('/words', '')
    for word in text.split():
        total_words += 1

    await message.answer("Thinking. . .")
    user_word = message.text

    # Dictionary answer
    if total_words == 1:

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
            pick_emoji = random.choice(cldr_emoji_name)
            translation = translator.translate(word)
            await message.reply(f"{emoji.emojize(pick_emoji)} Your word is: {word} ({translation})\n\n"
                                "Sorry, but this word is not in the dictionary")
   
    # Translation 
    elif total_words > 1:
        
        pick_emoji = random.choice(cldr_emoji_name)
        translation = translator.translate(user_word)
        response = f"{emoji.emojize(pick_emoji)} Your words: {user_word}\n\nTranslation: {translation}"

        await message.reply(response)

    else:
        await message.reply(f"❌ There is no word/words\n"
                            "Type /help if you need some insctrutions")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
