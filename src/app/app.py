import openai
import telebot
import bot_token
import api_key
from telebot import types
from model import model
from pyclickhouse import Connection

openai.api_key = api_key.key
bot = telebot.TeleBot(bot_token.token)
max_tokens = 128

connection = Connection(
        host='localhost',
        port=8123,
    )


def request(call):
    bot.answer_callback_query(call.id, "Вы нажали кнопку \"Начать диалог\"")
    bot.send_message(call.message.chat.id, "Пожалуйста, напишите Ваш вопрос!")
    bot.register_next_step_handler(call.message, new_dialog)


def info(call):
    bot.answer_callback_query(call.id, "Вы выбрали info")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))
    bot.send_message(call.message.chat.id, "Данный бот может пообщаться с Вами на различные темы. Также он будет "
                                           "рад помочь вам с помощью советов и мотивации"
                                           "\n\nGive it a try :)", reply_markup=keyboard)


def menu(call):
    bot.answer_callback_query(call.id, "Вы вернулись в меню")
    bot.send_message(call.message.chat.id, "Вы вернулись в меню")


# "id:" = message.from_user.id
# send you a message with the inline keyboard
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup(row_width=7)
    keyboard.add(types.InlineKeyboardButton(text="Начать диалог на любую тему", callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Найти интересные вакансии", callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Улучшить резюме под конкретную вакансию", callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Пройти собеседование", callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Получить feedback по своему резюме", callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Зарядиться мотивацией", callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Анализ рынка по вакансии", callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Развитие",
                                            callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Получить информацию о компании", callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Как вести себя во время собеседования", callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Психологически-успокаивающее общение после собеса",
                                            callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Info", callback_data="info"))
    bot.send_message(message.from_user.id, "Привет!\nМеня зовут getJobBot, я помогу Вам найти работу мечты и "
                                           "расширить горизонт!\nВыбирайте интересующие тебя опции из списка ниже, "
                                           " и получай очки за выполнение заданий\nВаши показатели будут мотивировать "
                                           "Вас двигаться дальше!", reply_markup=keyboard)


# hook the user's button request
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "request":
        request(call)
    elif call.data == "info":  # if user choose info button
        info(call)
    elif call.data == "key_yes":
        menu(call)
        # send_welcome(call.message)
    else:
        bot.answer_callback_query(call.id, "Вы не нажимали кнопок")


# if user choose new dialog button
@bot.message_handler(func=lambda m: True)
def new_dialog(message):
    message_from_user = message.text
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))
    inputFromUser = str(message_from_user)
    outputFromModel = str(model(message_from_user, max_tokens).choices[0].text)
    cursor = connection.cursor()
    insert_query = "INSERT INTO chat  VALUES ('{}', '{}')".format(inputFromUser, outputFromModel)
    cursor.execute(insert_query)
    bot.send_message(message.from_user.id, outputFromModel, reply_markup=keyboard)


if __name__ == '__main__':
    # bot.polling(none_stop=True)
    bot.polling(none_stop=True, interval=0)
