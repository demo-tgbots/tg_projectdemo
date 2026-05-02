from telebot import types
import telebot
bot = telebot.TeleBot("8590465306:AAH2QdfOzvj9bOJGqdVF7knXTapqMGOJ8Lw")

ADMINS = [1729484185,987654321]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в магазин одежды 👕')

    markup = types.InlineKeyboardMarkup(row_width=2)

    markup1 = types.InlineKeyboardButton('🛍 Каталог', callback_data='katalog')
    markup2 = types.InlineKeyboardButton('📦 Мои заказы', callback_data='order')
    markup3 = types.InlineKeyboardButton('ℹ️ О нас', callback_data='faq')

    markup.add(markup1, markup2, markup3)

    bot.send_message(message.chat.id, "Выберите:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == 'katalog':
        bot.send_message(call.message.chat.id, "Перенаправляем в каталог")
        katalogi(call.message)

    elif call.data == 'order':
        bot.send_message(call.message.chat.id, "Перенаправляем в заказы")

    elif call.data == 'faq':
        bot.send_message(call.message.chat.id, "Перенаправляем в информацию")

    elif call.data in ['Кофта','Джинсы','Куртка']:
        bot.send_message(call.message.chat.id,'Какое ваше имя?')
        bot.register_next_step_handler(call.message,phone,call.data)
    elif call.data == 'back':
        start(call.message)

def katalogi(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup12 = types.InlineKeyboardButton('Кофта PIDORAS 6700р', callback_data='Кофта')
    markup23 = types.InlineKeyboardButton('Джинсы Maison VIKA OGROMNAYA ZOPA 67: 13990', callback_data='Джинсы')
    markup34 = types.InlineKeyboardButton('Куртка SAVS: 15999', callback_data='Куртка')
    markup35 = types.InlineKeyboardButton('Назад',callback_data='back')

    markup.add(markup12, markup23, markup34, markup35)

    bot.send_message(message.chat.id, "Каталог:", reply_markup=markup)


def phone(message,product):
    name = message.text
    bot.send_message(message.chat.id,'Какой ваш номер телефона?') 
    bot.register_next_step_handler(message,email,product,name)
def email(message,product,name):
    phone = message.text
    bot.send_message(message.chat.id,'Введите ваш email')
    bot.register_next_step_handler(message,final,product,name,phone)
def final(message,product,name,phone):
    email = message.text
    text = f'''
        Новый заказ!
        товар: {product}
        Имя: {name}
        Email: {email}
        Phone: {phone}'''
    for admin in ADMINS:
        bot.send_message(admin, text)

bot.polling(none_stop=True)
