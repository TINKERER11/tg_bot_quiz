import telebot
from toke import TOKEN
import time


class UserState(telebot.handler_backends.StatesGroup):
    kol_p = telebot.handler_backends.State()
    shrek = telebot.handler_backends.State()
    dog = telebot.handler_backends.State()


def prov(call: telebot.types.CallbackQuery) -> bool:
    return not (call in ["Мамонт", "Чебурашка", "Фиксики", "Леопольд", "Алёша Попович", "Мурка", "Винни-Пух"])


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}!\n"
                                                f"Этот бот создан для проведения"
                                                f" викторины на знание мультфильмов.", parse_mode='HTML')
    time.sleep(1)
    bot.send_message(message.chat.id, text=f"Для того, чтобы <i>начать викторину</i> нажмите на /begin",
                     parse_mode='HTML')


@bot.message_handler(commands=['begin'])
def begin_quiz(message: telebot.types.Message):
    markup = telebot.util.quick_markup(
        {
            "Мамонт": {"callback_data": "Мамонт"},
            "Слон": {"callback_data": "Слон"}
        }
    )
    bot.reply_to(message, text='<b><u>Самое крупное животное из'
                               ' мультфильма "Ледниковый период"...</u></b>', parse_mode="HTML", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "Мамонт")
def cal_1(message: telebot.types.Message):
    bot.send_message(message.from_user.id, text="<b>Правильно!</b>", parse_mode='HTML')
    time.sleep(1)
    with open("photo1.jpg", "rb") as photo:
        bot.send_message(message.from_user.id, text="Сколько попугаев в удаве?", parse_mode='HTML')
        bot.send_photo(message.from_user.id, photo)
    bot.set_state(message.from_user.id, UserState.kol_p, message.from_user.id)


@bot.message_handler(state=UserState.kol_p)
def kolichestvo(message: telebot.types.Message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['kol'] = message.text
    try:
        kol = int(data['kol'])
    except Exception:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.from_user.id, text="Вы ввели не число!", parse_mode='HTML')
        bot.set_state(message.from_user.id, UserState.kol_p, message.chat.id)
    else:
        if kol == 38:
            bot.send_message(message.from_user.id, text="Верно!", parse_mode='HTML')
            markup = telebot.util.quick_markup(
                {
                    "Шапокляк": {"callback_data": "Шапокляк"},
                    "Незнайка": {"callback_data": "Незнайка"},
                    "Чебурашка": {"callback_data": "Чебурашка"},
                    "Карлсон": {"callback_data": "Карлсон"}
                }
            )
            bot.reply_to(message, text="Кто в телефонной будке жил,\n"
                                       "Пел песни, с Геною дружил?\n"
                                       "Он мягкими ушами\n"
                                       "Запомнился нам с вами", parse_mode='HTML', reply_markup=markup)
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id, text="Неправильно...", parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == "Чебурашка")
def cal_2(callback: telebot.types.CallbackQuery):
    bot.send_message(callback.from_user.id, text="Очень хорошо!", parse_mode='HTML')
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("Шарик"),
        telebot.types.KeyboardButton("Стрелка"),
        telebot.types.KeyboardButton("Белка и Стрелка"),
        telebot.types.KeyboardButton("Арчо")
    )
    bot.send_message(callback.from_user.id, text="Какая(ие) собака(и) летала(и) в космос?", parse_mode='HTML',
                     reply_markup=markup)
    bot.set_state(callback.from_user.id, UserState.dog, callback.from_user.id)


@bot.message_handler(state=UserState.dog)
def cal_3(message: telebot.types.Message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['dog'] = message.text
    dog = data['dog']
    if dog.lower() == "белка и стрелка":
        markup1 = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, text="Молодец", reply_markup=markup1)
        markup = telebot.util.quick_markup(
            {
                "Чип и Дейл": {"callback_data": "Чип и Дейл"},
                "Фиксики": {"callback_data": "Фиксики"},
                "Том и Джери": {"callback_data": "Том и Джери"}
            }
        )
        bot.send_message(message.from_user.id, text="Как называется мультфильм о маленьких человечках, которые живут "
                                                    "внутри приборов и в машинах, "
                                                    "они ухаживают за техникой и устраняют "
                                                    "неполадки, они часто превращаются "
                                                    "в винтики, чтоб люди не смогли о "
                                                    "них узнать", parse_mode='HTML', reply_markup=markup)
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, text="Неправильно...")


@bot.callback_query_handler(func=lambda call: call.data == "Фиксики")
def cal_4(callback: telebot.types.CallbackQuery):
    bot.send_message(callback.from_user.id, text="Правильно!", parse_mode='HTML')
    time.sleep(1)
    markup = telebot.util.quick_markup(
        {
            "Котёнок Гав": {"callback_data": "Котёнок Гав"},
            "Том": {"callback_data": "Том"},
            "Леопольд": {"callback_data": "Леопольд"}
        }
    )
    bot.send_message(callback.from_user.id, text="Чья цитата?\n"
                                                 "<blockquote>Ребята, давайте жить дружно!</blockquote>",
                     parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "Леопольд")
def cal_5(callback: telebot.types.CallbackQuery):
    bot.send_message(callback.from_user.id, text="Верно.", parse_mode='HTML')
    time.sleep(1)
    bot.send_message(callback.from_user.id, text="Какой герой стал мужем принцессы Фионы?", parse_mode='HTML')
    bot.set_state(callback.from_user.id, UserState.shrek, callback.from_user.id)


@bot.message_handler(state=UserState.shrek)
def shr(message: telebot.types.Message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['shrek'] = message.text
    shrek = data['shrek']
    if shrek.lower() == "шрек":
        bot.send_message(message.from_user.id, text="Perfect!", parse_mode='HTML')
        time.sleep(1)
        markup = telebot.util.quick_markup(
            {
                "Николай II": {"callback_data": "Николай II"},
                "Алёша Попович": {"callback_data": "Алёша Попович"},
                "Микула Селянович": {"callback_data": "Микула Селянович"}
            }
        )
        bot.send_message(message.from_user.id, text="Кто из этих людей богатырь?", parse_mode='HTML',
                         reply_markup=markup)
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, text="Неправильно...")


@bot.callback_query_handler(func=lambda call: call.data == "Алёша Попович")
def cal_6(callback: telebot.types.CallbackQuery):
    bot.send_message(callback.from_user.id, text="Верно!", parse_mode='HTML')
    markup = telebot.util.quick_markup(
        {
            "Мурка": {"callback_data": "Мурка"},
            "Милка": {"callback_data": "Милка"},
            "Бурёнка": {"callback_data": "Бурёнка"}
        }
    )
    bot.send_message(callback.from_user.id, text="Как называл свою корову кот Матроскин?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "Мурка")
def cal_7(callback: telebot.types.CallbackQuery):
    bot.send_message(callback.from_user.id, text="Молодец!")
    markup = telebot.util.quick_markup(
        {
            "Винни-Пух": {"callback_data": "Винни-Пух"},
            "Кунг-фу панда": {"callback_data": "Кунг-фу панда"},
            "Братец медвежонок": {"callback_data": "Братец медвежонок"}
        }
    )
    bot.send_message(callback.from_user.id, text="<blockquote>Для него прогулки- праздник,\n"
                                                 "И на мед особый нюх.\n"
                                                 "Это плюшевый проказник,\n"
                                                 "Медвежонок …</blockquote>", parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "Винни-Пух")
def cal_8(callback: telebot.types.CallbackQuery):
    bot.send_message(callback.from_user.id, text="Молодец!", parse_mode='HTML')
    time.sleep(1)
    bot.send_message(callback.from_user.id, text="Итак, викторина завершена!")
    time.sleep(1)
    for i in range(5, 0, -1):
        bot.send_message(callback.from_user.id, text=f"<b>{i}</b>", parse_mode='HTML')
        time.sleep(1)
    bot.send_message(callback.from_user.id, text=f"{callback.from_user.first_name} прошел(а)"
                                                 f" <b>викторину</b> {time.ctime()}",
                     parse_mode='HTML')


@bot.callback_query_handler(func=prov)
def cal_9(callback: telebot.types.CallbackQuery):
    bot.send_message(callback.from_user.id, text="Неверно...")


bot.add_custom_filter(telebot.custom_filters.StateFilter(bot))
bot.infinity_polling()