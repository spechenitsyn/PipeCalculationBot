import telebot
from pipe_calculation import pipe_calculation

TOKEN = "6050002447:AAFSnC3qp1on3AgLMbjZ-dO3tPHiJWrTers"
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
def diameter(message):
    diam = message.text
    if float(diam) > 0:
        bot.send_message(message.chat.id, "<b>Введите толщину стенки (мм)</b>", parse_mode='html')
        bot.register_next_step_handler(message, thickness, diam)
    else:
        bot.send_message(message.chat.id, "Диаметр должен быть больше 0")


@bot.message_handler(content_types=['text'])
def thickness(message, diam):
    thick = message.text
    result = round(pipe_calculation(diam, thick), 2)
    bot.send_message(message.chat.id, f"Результат равен: {result} кг")


bot.polling(non_stop=True)
