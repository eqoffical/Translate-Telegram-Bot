import config
import emoji
import random
import logging
import asyncio
import string
from aiogram import Bot, Dispatcher, executor, types
from PyDictionary import PyDictionary
from deep_translator import GoogleTranslator

cldr_emoji_name = list(emoji.EMOJI_DATA.keys()) 
logging.basicConfig(level=logging.INFO) # log
bot = Bot(token=config.TOKEN) # init aiogram
dp = Dispatcher(bot)
dictionary = PyDictionary()
translator = GoogleTranslator(source='en', target='uk')
reverse_translator = GoogleTranslator(source='uk', target='en')

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

    # language check
    UKRAINIAN_LETTERS = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя'-"
    ENGLISH_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-"

    for character in user_word:
        
        if character in UKRAINIAN_LETTERS + " ":
            this_is_ukrainian_text = 1
            this_is_english_text = 0

        elif character in ENGLISH_LETTERS + " ":
            this_is_ukrainian_text = 0
            this_is_english_text = 1

        elif character in UKRAINIAN_LETTERS + ENGLISH_LETTERS + " ":
            this_is_ukrainian_text = 1
            this_is_ukrainian_text = 1

        else:
            this_is_ukrainian_text = 0
            this_is_english_text = 0

    # # Debug
    # await message.reply(f"En: {this_is_english_text}, Uk: {this_is_ukrainian_text}")

    # Dictionary answer
    if total_words == 1:

        try:

            if this_is_english_text == 1 and this_is_ukrainian_text == 0:
                word = user_word

            elif this_is_english_text == 0 and this_is_ukrainian_text == 1:
                
                # word = reverse_translator.translate(user_word) <-- 
                
                translated = reverse_translator.translate(user_word)
                translated_words = translated.split(' ')
                word = max(translated_words, key=len)

            translation = translator.translate(word)
            meanings = dictionary.meaning(word)
            pick_emoji = random.choice(cldr_emoji_name)

            response = f"{emoji.emojize(pick_emoji)} Your word is: {word}\n💬 Translation: {translation}\n"
            # response = f"{word} - {translation}\n\n{dictionary.meaning(word)}"
        
            for part_of_speech, definitions in meanings.items():
                response += f"\n{part_of_speech}:\n"
                for definition in definitions:
                    clean_def = definition.translate(str.maketrans('', '', '[]()'''))
                    response += f"• {clean_def}\n"

            await message.reply(response)

        except: 

            pick_emoji = random.choice(cldr_emoji_name)
            translation = translator.translate(word)
            
            response = f"{emoji.emojize(pick_emoji)} Your word is: {word} \n💬 Possible translation: {translation}\n\n"
            apologies = f"Sorry, but this word is not in the dictionary\nYou can try type \"{user_word}\" in a different way"
            
            await message.reply(response + apologies)
   
    # Translation 
    elif total_words > 1:
        
        pick_emoji = random.choice(cldr_emoji_name)
        translation = translator.translate(user_word)
        response = f"{emoji.emojize(pick_emoji)} Your words: {user_word}\n\n💬 Translation: {translation}"

        await message.reply(response)

    else:
        await message.reply(f"❌ There is no word/words\n"
                            "Type /help if you need some insctrutions")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
