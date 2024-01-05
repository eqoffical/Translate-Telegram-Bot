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
    await message.answer(f"Hello {first_name} 👋\n\n"
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
    
    text = message.text 
    
    total_words = 0
    total_characters = 0
    word_limit = 256
    characters_limit = 45
    
    for word in text.split():
        total_words += 1

    for character in text:  
        total_characters += 1

    await message.answer("Thinking. . .")
    user_word = message.text

    # language check
    UKRAINIAN_LETTERS = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя'-"
    ENGLISH_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-"

    ukrainian_count = 0
    english_count = 0
    
    for character in text:
        if character in UKRAINIAN_LETTERS:
            ukrainian_count += 1
        if character in ENGLISH_LETTERS:  
            english_count += 1

    if ukrainian_count > 0:
        this_is_ukrainian_text = True
    else:
        this_is_ukrainian_text = False

    if english_count > 0:
        this_is_english_text = True  
    else:
        this_is_english_text = False

    # # Debug
    # await message.reply(f"En: {this_is_english_text}, Uk: {this_is_ukrainian_text}")

    # Dictionary answer
    if total_words == 1 and total_characters <= characters_limit:

        try:

            if this_is_english_text == True and this_is_ukrainian_text == False:
                word = user_word

            elif this_is_english_text == False and this_is_ukrainian_text == True:
                
                # word = reverse_translator.translate(user_word) <-- 
                
                translated = reverse_translator.translate(user_word)
                translated_words = translated.split(' ')
                word = max(translated_words, key=len)

            translation = translator.translate(word)
            meanings = dictionary.meaning(word)
            pick_emoji = random.choice(cldr_emoji_name)

            response = f"{emoji.emojize(pick_emoji)} The word: {word}\n\n💬 Translation: {translation}\n"
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
            
            response = f"{emoji.emojize(pick_emoji)} The word: {word}\n\n💬 Translation: {translation}\n\n"
            apologies = f"💡 Sorry, but this word is not in the dictionary\nYou can try type \"{user_word}\" in a different way"
            
            await message.reply(response + apologies)
    
    elif total_characters > characters_limit:
        
        response = f"💡 Sorry, but you have reached the characters limit, the maximum number of characters in single word is {characters_limit}"
        await message.reply(response)

    # Translation 
    elif total_words > 1 and total_words < word_limit:

        if this_is_english_text == True and this_is_ukrainian_text == False:
            word = user_word
            post_text = ""

        elif this_is_english_text == False and this_is_ukrainian_text == True:
            word = reverse_translator.translate(user_word)
            post_text = ""

        elif this_is_english_text == True and this_is_ukrainian_text == True:
            word = reverse_translator.translate(user_word)
            post_text = "⚠ Please, don't send english and ukrainian at the same time"
            
        pick_emoji = random.choice(cldr_emoji_name)
        translation = translator.translate(user_word)
        response = f"{emoji.emojize(pick_emoji)} The text: {word}\n\n💬 Translation: {translation}\n\n{post_text}"

        await message.reply(response)

    elif total_words > word_limit:

        response = f"💡 Sorry, but you have reached the word limit, the maximum number of words is {word_limit}"
        await message.reply(response)

    else:
        await message.reply(f"❌ There is no word/words\n"
                            "Type /help if you need some insctrutions")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
