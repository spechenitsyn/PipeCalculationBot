import telebot
from pipe_calculation import pipe_calculation
from pipe_calculation import check_data
from telebot.types import Message
import os

TOKEN = os.getenv('PIPE_TOKEN')
bot = telebot.TeleBot(TOKEN)

bot.set_my_commands([telebot.types.BotCommand("/start_bot", "Ввести данные")])


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет, <b>{message.from_user.first_name}</b>. Я помогу тебе рассчитать "
                                      "массу погонного метра стальной бесшовной трубы."
                                      "Нажми начать расчёт для ввода данных", parse_mode='html')


@bot.message_handler(commands=['start_bot'])
def input_data(message):
    bot.send_message(message.chat.id, "<b>Введите диаметр (мм)</b>", parse_mode='html')
    bot.register_next_step_handler(message, diameter)


@bot.message_handler(content_types=['text'])
def diameter(message: Message):
    diam = message.text
    if check_data(diam):
        bot.send_message(message.chat.id, "<b>Введите толщину стенки (мм)</b>", parse_mode='html')
        bot.register_next_step_handler(message, thickness, diam)
    else:
        bot.send_message(message.chat.id, "Диаметр должен быть больше 0")


def thickness(message: Message, diam):
    thick = message.text
    if check_data(thick) and float(thick) < float(diam):
        result = round(pipe_calculation(diam, thick), 2)
        bot.send_message(message.chat.id, f"<i>Масса погонного метра трубы равна: "
                                          f"{result} кг</i>", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Вы ввели некорректные данные. Попробуйте заново")


bot.polling(non_stop=True)
