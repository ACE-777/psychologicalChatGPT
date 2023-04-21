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

# build menu buttons
commands = [
    telebot.types.BotCommand('start', 'Вернуться в меню'),
]

bot.set_my_commands(commands)


def menu(call):
    bot.send_message(call.message.chat.id, "Выберете соответсвующую команду /start в кнопке menu или просто нажмите на"
                                           " нее в данном сообщении ")


# send you a message with the inline keyboard
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup(row_width=7)
    keyboard.add(types.InlineKeyboardButton(text="Профиль", callback_data="profile"))
    keyboard.add(types.InlineKeyboardButton(text="Найти интересные вакансии", callback_data="find_new_offers"))
    keyboard.add(types.InlineKeyboardButton(text="Улучшить резюме под конкретную вакансию", callback_data="upgrade_cv"))
    keyboard.add(types.InlineKeyboardButton(text="Скоро. Пройти собеседование", callback_data="info"))
    keyboard.add(types.InlineKeyboardButton(text="Скоро. Получить feedback по своему резюме", callback_data="info"))
    keyboard.add(types.InlineKeyboardButton(text="Скоро. Развитие", callback_data="info"))
    keyboard.add(types.InlineKeyboardButton(text="Скоро. Психологически-успокаивающее общение после собеседования",
                                            callback_data="info"))
    keyboard.add(types.InlineKeyboardButton(text="Список дел", callback_data="info"))
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
    elif call.data == "profile":
        profile(call)
    elif call.data == "C++":
        edit_profile_add_tag_C_plus(call)
    elif call.data == "find_new_offers":
        find_new_offers(call)
    elif call.data == "tags_offers":
        found_new_offers_with_tags(call)
        # found_new_offers_no_tags(call)
    elif call.data == "no_tags_offers":
        found_new_offers_no_tags(call)
    elif call.data == "get_interesting_links_from_user_response":
        interesting_offers_from_user(call)
    elif call.data == "upgrade_cv":
        upgrade_cv(call)
    elif call.data == "get_cv":
        get_data_of_cv(call)
    elif call.data == "get_link_of_job_vacancy_to_get_feedback_by_person":
        get_link_of_job_vacancy_person(call)
    elif call.data == "get_link_of_job_vacancy_to_get_feedback_by_GPT":
        get_link_of_job_vacancy_gpt(call)
    else:
        bot.answer_callback_query(call.id, "Вы не нажимали кнопок")


def profile(call):
    bot.answer_callback_query(call.id, "Вы нажали кнопку \"Профиль\"")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="C++", callback_data="C++"))
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    bot.send_message(call.message.chat.id, "Пожалуйста, выберете теги, присущие Вам.\n"
                                           "Вы можете получить за это 10 очков!", reply_markup=keyboard)


@bot.message_handler(func=lambda m: True)
def edit_profile_add_tag_C_plus(message):
    keyboard = types.InlineKeyboardMarkup()

    connection.open()
    cursor = connection.cursor()
    insert_query = "INSERT INTO chat.users_info (user_id,tags) VALUES ('{}','{}')".format(int(message.from_user.id),
                                                                                          "C++")
    cursor.execute(insert_query)
    connection.close()

    bot.send_message(message.from_user.id, "Ты получил 10 очков!", reply_markup=keyboard)


# if user choose new dialog button
def request(call):
    bot.answer_callback_query(call.id, "Вы нажали кнопку \"Начать диалог\"")

    bot.send_message(call.message.chat.id, "Пожалуйста, напишите Ваш вопрос!")

    bot.register_next_step_handler(call.message, new_dialog)


@bot.message_handler(func=lambda m: True)
def new_dialog(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    inputFromUser = str(message.text)
    outputFromModel = str(model(message.text, max_tokens).choices[0].text)
    connection.open()
    cursor = connection.cursor()
    insert_query = "INSERT INTO chat.job  VALUES ('{}', '{}')".format(inputFromUser, outputFromModel)
    cursor.execute(insert_query)
    connection.close()

    bot.send_message(message.from_user.id, outputFromModel, reply_markup=keyboard)


def find_new_offers(call):
    bot.answer_callback_query(call.id, "Вы нажали кнопку \"Найти интересные вакансии\"")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Ресурсы по тегам", callback_data="tags_offers"))
    keyboard.add(types.InlineKeyboardButton(text="Ресурсы не использая мои теги", callback_data="no_tags_offers"))
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    bot.send_message(call.message.chat.id, "Пожалуйста, выберете хотите ли вы подборку ресурсов по вашим тегам или "
                                           "нет.", reply_markup=keyboard)


@bot.message_handler(func=lambda m: True)
def found_new_offers_with_tags(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Прислать понравившиеся ссылки",
                                            callback_data="get_interesting_links_from_user_response"))
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    connection.open()
    cursor = connection.cursor()
    insert_query = "SELECT (tags) FROM chat.users_info WHERE user_id = '{}'".format(message.from_user.id)
    cursor.execute(insert_query)
    results = cursor.fetchall()

    links = []
    for item in results:
        insert_query = "SELECT (job_services) FROM chat.useful_links WHERE fields = '{}'".format(item['tags'])
        cursor.execute(insert_query)
        results = cursor.fetchall()
        for link_from_db in results:
            links.append(link_from_db['job_services'])

    links = list(set(links))
    output = '\n'.join(links)
    connection.close()
    bot.send_message(message.from_user.id, "Вот ресурсы на которых ты можешь найти интерсные вакансии. Можешь сходить "
                                           "на них и прислать мне понравившиеся тебе ссылки. Ты получишь за это 10 "
                                           "очков!\n" + output, reply_markup=keyboard)


@bot.message_handler(func=lambda m: True)
def found_new_offers_no_tags(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Прислать понравившиеся ссылки",
                                            callback_data="get_interesting_links_from_user_response"))
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    connection.open()
    cursor = connection.cursor()
    insert_query = 'SELECT (job_services) FROM chat.useful_links'
    cursor.execute(insert_query)
    results = cursor.fetchall()
    connection.close()

    output = '\n'.join([item['job_services'] for item in results])

    bot.send_message(message.from_user.id, "Вот ресурсы на которых ты можешь найти интерсные вакансии. Можешь сходить "
                                           "на них и прислать мне понравившиеся тебе ссылки. Ты получишь за это 10 "
                                           "очков!\n" + output, reply_markup=keyboard)


def interesting_offers_from_user(call):
    bot.send_message(call.message.chat.id, "Пожалуйста, пришлите понравившиеся Вам ссылки!")

    bot.register_next_step_handler(call.message, conversation_no_find_new_offers_response_with_links_from_user)


@bot.message_handler(func=lambda m: True)
def conversation_no_find_new_offers_response_with_links_from_user(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    connection.open()
    cursor = connection.cursor()
    insert_query = "INSERT INTO chat.users_info (user_id,users_desired_vacancies) VALUES ('{}','{}')".format(
        int(message.from_user.id), message.text)
    cursor.execute(insert_query)
    insert_query = "INSERT INTO chat.users_points VALUES ('{}','{}')".format(int(message.from_user.id), 10)
    cursor.execute(insert_query)
    connection.close()

    bot.send_message(message.from_user.id, "Ты получил 10 очков!", reply_markup=keyboard)


def upgrade_cv(call):
    bot.answer_callback_query(call.id, "Вы нажали кнопку \"Улучшить резюме под конкретную вакансию\"")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Пожалуйста, пришлите ссылку или в виде текста Ваше резюме!",
                                            callback_data="get_cv"))
    keyboard.add(types.InlineKeyboardButton(text="Получить советы по улучшению резюме",
                                            callback_data="advice_for_uprade_the_cv"))
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    bot.send_message(call.message.chat.id, "Пожалуйста, выберете один из перечисленных вариантов"
                                           "нет.", reply_markup=keyboard)


def get_data_of_cv(call):
    bot.send_message(call.message.chat.id, "Пожалуйста, пришлите ссылку или в виде текста Ваше резюме!")

    bot.register_next_step_handler(call.message, save_user_cv_and_wait_for_job_offer)


@bot.message_handler(func=lambda m: True)
def save_user_cv_and_wait_for_job_offer(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Получить сейчас feedback по улучшению резюме от ChatGPT",
                                            callback_data="get_link_of_job_vacancy_to_get_feedback_by_GPT"))
    keyboard.add(types.InlineKeyboardButton(text="Получить позже feedback по улучшению резюме от человека",
                                            callback_data="get_link_of_job_vacancy_to_get_feedback_by_person"))
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    connection.open()
    cursor = connection.cursor()
    insert_query = "INSERT INTO chat.users_cv (user_id, user_cv ) VALUES ('{}','{}')".format(
        int(message.from_user.id), message.text)
    cursor.execute(insert_query)
    connection.close()

    bot.send_message(message.from_user.id, "Пожалуйста выберете одни из предлогаемых вариантов!", reply_markup=keyboard)


def get_link_of_job_vacancy_person(call):
    bot.answer_callback_query(call.id, "Вы нажали кнопку \"Получить позже feedback по улучшению резюме от человека\"")
    bot.send_message(call.message.chat.id, "Пожалуйста, пришлите ссылку на вакансию!")

    bot.register_next_step_handler(call.message, new_dialog)

    bot.register_next_step_handler(call.message, get_link_of_job_vacancy_person_for_save_in_clickhouse)


@bot.message_handler(func=lambda m: True)
def get_link_of_job_vacancy_person_for_save_in_clickhouse(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    connection.open()
    cursor = connection.cursor()
    insert_query = "INSERT INTO chat.users_info (user_id, scope_of_job_search ) VALUES ('{}','{}')".format(
        int(message.from_user.id), message.text)
    cursor.execute(insert_query)
    connection.close()

    bot.send_message(message.from_user.id, "Спасибо, ожидайте проверки Вашего резюме!", reply_markup=keyboard)


def get_link_of_job_vacancy_gpt(call):
    bot.answer_callback_query(call.id, "Вы нажали кнопку \"Получить сейчас feedback по улучшению резюме от ChatGPT\"")
    bot.send_message(call.message.chat.id, "Пожалуйста, пришлите ссылку на вакансию!")

    bot.register_next_step_handler(call.message, new_dialog)

    bot.register_next_step_handler(call.message, get_link_of_job_vacancy_and_response_gpt)


@bot.message_handler(func=lambda m: True)
def get_link_of_job_vacancy_and_response_gpt(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    connection.open()
    cursor = connection.cursor()
    insert_query = "SELECT (user_cv) FROM chat.users_cv WHERE user_id = '{}'".format(message.from_user.id)
    cursor.execute(insert_query)
    results = cursor.fetchall()
    cv = []
    for link_from_db in results:
        cv.append(link_from_db['user_cv'])

    outputFromModel = str(model("Улучши резюме:\n"+cv[0]+"\nПо вакансии:\n"+message.text, max_tokens).choices[0].text)

    bot.send_message(message.from_user.id, outputFromModel, reply_markup=keyboard)


def info(call):
    bot.answer_callback_query(call.id, "Вы выбрали info")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="key_yes"))

    bot.send_message(call.message.chat.id, "Данный бот может пообщаться с Вами на различные темы. Также он будет "
                                           "рад помочь вам с помощью советов и мотивации"
                                           "\n\nДостаточно просто попробовать! :)", reply_markup=keyboard)


# bot.polling(none_stop=True)
if __name__ == '__main__':
    # bot.polling(none_stop=True)
    bot.polling(none_stop=True, interval=0)
