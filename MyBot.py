import telebot
import Parcer, Translator, my_session, tables, Emails
from datetime import datetime
import time
import re
import schedule
import threading

Bot_Token = '1262424562:AAHllz92_9SXMDrI1oZsfcyP4On5Qa6BZ1g'
bot = telebot.TeleBot(Bot_Token)
my_translator = Translator.MyTranslator()
list_of_users, my_list_of_time = [], [[] for x in range(24)]
dollar_cur, euro_cur = '', ''
choose_language, choose_time, write_email = False, False, False
delete_keyboard = telebot.types.ReplyKeyboardRemove()
language_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
language_keyboard.row('English', 'Русский')
language_keyboard.row('Deutsch', '日本語')
language_keyboard.row('čeština', '中文')
language_keyboard.row('Français')
time_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
time_keyboard.row("6:00", "8:00", "10:00")
time_keyboard.row("12:00", "14:00", "16:00")
time_keyboard.row("18:00", "20:00", "22:00")
my_list_of_languages = {'English': '1',
                        'Русский': '0',
                        'Deutsch': '2',
                        '日本語': '3',
                        'čeština': '5',
                        '中文': '6',
                        'Français': '4'}


@bot.message_handler(commands=['start'])
def start(message):
    session = my_session.create_session()
    if message.chat.id not in list_of_users:
        chat = tables.Chat()
        chat.id = message.chat.id
        chat.language = '1'
        chat.email = ''
        session.add(chat)
        session.commit()
        list_of_users.append(message.chat.id)
    user = message.from_user.username
    language = my_session.my_request(message.chat.id).language
    if user is None:
        user = str(my_translator.translate(4, language))
    phrase = str(my_translator.translate(1, language))
    bot.send_message(message.chat.id, text=str(phrase + ' ' + user + "!"), reply_markup=delete_keyboard)


@bot.message_handler(commands=['dollar'])
def dollar(message):
    global choose_language, choose_time, write_email, dollar_cur
    choose_language, choose_time, write_email = False, False, False
    language = my_session.my_request(message.chat.id).language
    phrase = my_translator.translate(dollar_cur, language)
    bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)


@bot.message_handler(commands=['euro'])
def euro(message):
    global choose_language, choose_time, write_email, euro_cur
    choose_language, choose_time, write_email = False, False, False
    language = my_session.my_request(message.chat.id).language
    phrase = my_translator.translate(euro_cur, language)
    bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)


@bot.message_handler(commands=['language'])
def language(message):
    global choose_language, choose_time, write_email
    language = my_session.my_request(message.chat.id).language
    phrase = my_translator.translate(2, language)
    choose_language, choose_time, write_email = True, False, False
    bot.send_message(message.chat.id, text=phrase, reply_markup=language_keyboard)


@bot.message_handler(commands=['time'])
def my_time(message):
    global choose_language, choose_time, write_email
    language = my_session.my_request(message.chat.id).language
    choose_language, choose_time, write_email = False, True, False
    phrase = my_translator.translate(5, language)
    bot.send_message(message.chat.id, text=phrase, reply_markup=time_keyboard)


@bot.message_handler(commands=['add_email'])
def email(message):
    global choose_time, choose_language, write_email
    language = my_session.my_request(message.chat.id).language
    choose_language, choose_time, write_email = False, False, True
    phrase = my_translator.translate(9, language)
    bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)


@bot.message_handler(commands=['delete_email'])
def delete_email(message):
    global choose_language, choose_time, write_email
    choose_language, choose_time, write_email = False, False, False
    session = my_session.create_session
    chat = session.query(tables.Chat).filter(tables.Chat.id == id).first()
    chat.email = ''
    session.commit()
    phrase = my_translator.translate(8, chat.language)
    bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)


@bot.message_handler(commands=['info'])
def info(message):
    global choose_language, choose_time, write_email
    choose_language, choose_time, write_email = False, False, False
    language = my_session.my_request(message.chat.id).language
    phrase = my_translator.translate(7, language)
    bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)


@bot.message_handler(content_types=['text'])
def unknown(message):
    global choose_language, choose_time, write_email
    session = my_session.create_session()
    chat = session.query(tables.Chat).filter(tables.Chat.id == message.chat.id).first()
    if choose_language:
        try:
            chat.language = my_list_of_languages[message.text]
            session.commit()
            phrase = my_translator.translate(3, chat.language)
            choose_language = False
            bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)
        except Exception:
            language = chat.language
            phrase = my_translator.translate(0, language)
            choose_language = False
            bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)
    elif choose_time:
        try:
            chat.time = int(message.text[:-3])
            my_list_of_time[int(message.text[:-3])].append(chat.id)
            session.commit()
            language = chat.language
            phrase = my_translator.translate(6, language)
            choose_time = False
            bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)
        except Exception:
            language = chat.language
            phrase = my_translator.translate(0, language)
            choose_time = False
            bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)
    elif write_email:
        try:
            if Emails.check_email(message.text):
                chat.email = Emails.check_email(message.text)
                session.commit()
                language = chat.language
                phrase = my_translator.translate(11, language)
                bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)
            else:
                language = chat.language
                phrase = my_translator.translate(10, language)
                bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)
        except Exception:
            language = chat.language
            phrase = my_translator.translate(0, language)
            choose_time = False
            bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)
    else:
        language = chat.language
        phrase = my_translator.translate(0, language)
        bot.send_message(message.chat.id, text=phrase, reply_markup=delete_keyboard)


def run_bot():
    bot.polling()


def check_time(first_time=False):
    global dollar_cur, euro_cur
    if first_time or int(datetime.now().strftime("%H")) == 5:
        dollar_cur, euro_cur = Parcer.Currency().dollar_currency(), Parcer.Currency().euro_currency()
        print('Новые значения доллара и евро!')
    try:
        for element in my_list_of_time[int(datetime.now().strftime("%H"))]:
            language = my_session.my_request(message.chat.id).language
            dollar_now = my_translator.translate(dollar_cur, language)
            euro_now = my_translator.translate(euro_cur, language)
            phrase = f"{dollar_now}\n{euro_now}"
            bot.send_message(element, text=phrase, reply_markup=delete_keyboard)
    except Exception as exc:
        print(exc)


def run_scheduler():
    schedule.every().hour.at(":00").do(check_time)

    while True:
        schedule.run_pending()
        time.sleep(1)

# запуск бота
if __name__ == '__main__':
    check_time(first_time=True)
    bot_target = threading.Thread(target=run_bot)
    time_target = threading.Thread(target=run_scheduler)
    bot_target.start()
    time_target.start()