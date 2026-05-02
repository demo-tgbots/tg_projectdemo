import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot("8684655563:AAFyo7qxRzWUor8etFXL2hhZvJd2_5IwDVI")
ADMINS = [1729484185]

conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    phone TEXT,
    product TEXT
)
""")
conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в магазин одежды 👔')

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('🛍 Купить товар', callback_data='katalog'),
        types.InlineKeyboardButton('📦 Мои заказы', callback_data='orders')
    )

    bot.send_message(message.chat.id, 'Выберите☣️', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def calldata(call):

    if call.data == 'katalog':
        pokup(call.message)

    elif call.data in ['Футболка1', 'Худи1', 'Куртка1']:
        bot.send_message(call.message.chat.id, 'Как вас зовут?')
        bot.register_next_step_handler(call.message, name, call.data)

    elif call.data == 'back':
        start(call.message)

    elif call.data == 'orders':
        cursor.execute("""
            SELECT product, phone FROM orders
            WHERE user_id = ?
        """, (call.from_user.id,))

        rows = cursor.fetchall()

        if rows:
            text = "Ваш(и) заказ(ы):\n"
            for row in rows:
                text += f"{row[0]} | {row[1]}\n"
        else:
            text = "У вас нет заказов"

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='back'))

        bot.send_message(call.message.chat.id, text)
        bot.send_message(call.message.chat.id, 'Вернуться обратно?', reply_markup=markup)


def pokup(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('Футболка - 500р', callback_data='Футболка1'),
        types.InlineKeyboardButton('Худи - 1200р', callback_data='Худи1'),
        types.InlineKeyboardButton('Куртка - 2500р', callback_data='Куртка1')
    )

    bot.send_message(message.chat.id, 'Что хотите приобрести?', reply_markup=markup)


def name(message, product):
    user_name = message.text
    bot.send_message(message.chat.id, 'Какой ваш номер телефона?')
    bot.register_next_step_handler(message, phone, product, user_name)


def phone(message, product, user_name):
    user_phone = message.text
    final(message, product, user_name, user_phone)


def final(message, product, name, phone):

    
    cursor.execute("""
        INSERT INTO orders(user_id, name, phone, product)
        VALUES (?, ?, ?, ?)
    """, (message.from_user.id, name, phone, product))
    conn.commit()

  
    bot.send_message(message.chat.id, 'Спасибо за покупку!')

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Вернуться на главное меню', callback_data='back'))

    bot.send_message(message.chat.id, 'Вернуться на главное меню', reply_markup=markup)

    #
    for admin in ADMINS:
        bot.send_message(admin, f"""
НОВЫЙ ЗАКАЗ
ТОВАР: {product}
ИМЯ: {name}
ТЕЛЕФОН: {phone}
""")


bot.polling(non_stop=True)