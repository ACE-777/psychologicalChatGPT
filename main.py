import openai
import telebot
import bot_token
import api_key
from telebot import types

openai.api_key = api_key.key
bot = telebot.TeleBot(bot_token.token)
model_engine = "text-davinci-003"
max_tokens = 128


def model(prompt, max_tokens_in_model):
    """
            Creates a model based on Chat-GPT for the answering users questions.
    """
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens_in_model,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return completion


# send you a message with the inline keyboard
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Start dialog on any topic", callback_data="request"))
    keyboard.add(types.InlineKeyboardButton(text="Info", callback_data="info"))
    bot.send_message(message.from_user.id, "Hello! Choose one options buttons:", reply_markup=keyboard)


# hook the user's button request
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "request":
        bot.answer_callback_query(call.id, "You have pressed start dialog")
        bot.send_message(call.message.chat.id, "PLease write your request")
        bot.register_next_step_handler(call.message, new_dialog)
    elif call.data == "info":  # if user choose info button
        bot.answer_callback_query(call.id, "You have pressed info")
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Return to menu", callback_data="key_yes"))
        bot.send_message(call.message.chat.id, "This bot will have a conversation with you on various topics. "
                                               "He is also able to support you, motivate you, and provide advice! "
                                               "\n\nGive it a try :)", reply_markup=keyboard)
    elif call.data == "key_yes":
        bot.answer_callback_query(call.id, "You have returned to menu")
        bot.send_message(call.message.chat.id, "You have returned to menu")
    else:
        bot.answer_callback_query(call.id, "You haven't pressed button")


# if user choose new dialog button
@bot.message_handler(func=lambda m: True)
def new_dialog(message):
    message_from_user = message.text
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Return to menu", callback_data="key_yes"))
    bot.send_message(message.from_user.id, model(message_from_user, max_tokens).choices[0].text, reply_markup=keyboard)


if __name__ == '__main__':
    # bot.polling(none_stop=True)
    bot.polling(none_stop=True, interval=0)
