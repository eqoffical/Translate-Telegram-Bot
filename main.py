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
github_link = config.GITHUB_LINK
tg_link = config.TELEGRAM_LINK
dp = Dispatcher(bot)
dictionary = PyDictionary()
translator = GoogleTranslator(source='en', target='uk')
reverse_translator = GoogleTranslator(source='uk', target='en')

# /start command
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user = message.from_user
    first_name = user.first_name

    text = f"Привіт {first_name} 👋\n\n"
    text += "Я бот, який допоможе вам знайти визначення будь-якого слова!\nДо речі, приєднуйся до "
    text += "<a href='{}'>групи </a>".format(tg_link)
    text += "цього бота, ви можете запропонувати ідею або повідомити про проблему!\n\n"
    text += "Напишіть /help якщо вам необхідна допомога\n\n"
    text += "🐞 Якщо у вас виникли якісь проблеми, будь ласка, повідом про них"

    await message.answer(text, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)                        

# /help command
@dp.message_handler(commands=['help'])
async def cmd_start(message: types.Message):
    user = message.from_user
    first_name = user.first_name
    await message.reply("Щоб отримати визначення будь-якого слова, просто введіть його у чат.\n"
                        "Якщо їх декілька, то речення буде просто перекладено.\n\n"
                        "Також, якщо ви не отримали визначення слова або не отримали його переклад, ви можете спробувати написати його без дефізу або інших символів, які можуть спричинити проблему, і якщо ви все одно не отримаєте потрібну відповідь, будь ласка, повідомте про це розробнику 🙏\n\n"
                        "/report - дає посилання на групу цього бота та на репозиторій GitHub\n"
                        "/help - показує це повідомлення\n\n"
                        "🐞 Якщо у вас виникли будь-які інші проблеми, будь ласка, повідомте про них також")

# /report command
@dp.message_handler(commands=['report'])
async def cmd_start(message: types.Message):

    text = "Отже, щоб повідомити, ви можете написати в групу або створити проблему на GitHub:\n\n"
    text += "<a href='{}'>💌 Група</a>\n".format(tg_link)
    text += "<a href='{}'>🐞 Репозиторій GitHub</a>\n\n".format(github_link)
    text += "Щиро дякуємо за ваш відгук!"

    await message.answer(text, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)

# chatting
@dp.message_handler()
async def cmd_chat(message: types.Message):
    
    text = message.text 
    
    total_words = 0
    word_limit = 256
    
    for word in text.split():
        total_words += 1

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
    if total_words == 1:

        try:

            if this_is_english_text == True and this_is_ukrainian_text == False:
                word = user_word

            elif this_is_english_text == False and this_is_ukrainian_text == True:
                
                translated = reverse_translator.translate(user_word)
                translated_words = translated.split(' ')
                word = max(translated_words, key=len)

            translation = translator.translate(word)
            meanings = dictionary.meaning(word)
            pick_emoji = random.choice(cldr_emoji_name)

            response = f"{emoji.emojize(pick_emoji)} Слово: {word}\n\n💬 Переклад: {translation}\n"

            for part_of_speech, definitions in meanings.items():
                response += f"\n{part_of_speech}:\n"
                for definition in definitions:
                    clean_def = definition.translate(str.maketrans('', '', '[]()'''))
                    translated_def = translator.translate(clean_def) 
                    response += f"• {translated_def}\n"

            await message.reply(response)

        except: 

            pick_emoji = random.choice(cldr_emoji_name)
            translation = translator.translate(word)
            
            response = f"{emoji.emojize(pick_emoji)} Слово: {word}\n\n💬 Переклад: {translation}\n\n"
            apologies = f"💡 Вибачте, але цього слова немає у словнику\nВи можете спробувати ввести \"{user_word}\" іншим способом"
            
            await message.reply(response + apologies)

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
            post_text = "⚠ Будь ласка, не надсилайте англійську та українську мови одночасно"
            
        pick_emoji = random.choice(cldr_emoji_name)
        translation = translator.translate(user_word)
        response = f"{emoji.emojize(pick_emoji)} Текст: {word}\n\n💬 Переклад: {translation}\n\n{post_text}"

        await message.reply(response)

    elif total_words > word_limit:

        response = f"💡 Вибачте, але ви досягли ліміту слів, максимальна кількість слів становить {word_limit}"
        await message.reply(response)

    else:
        await message.reply(f"❌ Тут немає слова/слів\n"
                            "Напиши /help якщо тобі необхідна допомога")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
