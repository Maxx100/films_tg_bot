import telebot
from telebot import types

bot = telebot.TeleBot("")

"""menu = types.InlineKeyboardMarkup(row_width=3)
menu.add(
    types.InlineKeyboardButton(text='Hi!', callback_data='b1'),
    types.InlineKeyboardButton(text='Hello!', callback_data='b2')
)"""

films = {}


def data_import():
    with open("films.txt", "r", encoding="UTF-8") as f:
        flag = 0
        for _ in f.readlines():
            i = _.rstrip("\n")
            if i == "0":
                flag = 1
            elif flag == 1:
                films[i] = []
                flag = 2
            elif flag == 2:
                films[list(films.keys())[-1]].append(". ".join(i.split(". ")[1:]).replace(" | ", "\n"))
    print(films)


def back_button(text, chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Назад")
    markup.add(item)
    bot.send_message(chat_id, text, reply_markup=markup)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, друг!')
    main(message)


@bot.message_handler(commands=['back'])
def main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in films:
        item = types.KeyboardButton(i)
        markup.add(item)
    bot.send_message(message.chat.id, "Что ты хочешь посмотреть на сегодня?", reply_markup=markup)


@bot.message_handler()
def output(message):
    if message.text in films:
        for i in films[message.text]:
            bot.send_message(message.chat.id, i)
    else:
        bot.send_message(message.chat.id, "Извини, я не понимаю")


if __name__ == "__main__":
    data_import()
    bot.infinity_polling()
