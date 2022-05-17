import telebot
from telebot import types
from extensions import *
from config import *
import traceback

bot = telebot.TeleBot(TOKEN)

#Создаем функцию для создания клавиатуры
def create_markup(base=None):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for val in key.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.capitalize()))
    markup.add(*buttons)
    return markup

#Вывод сообщения для команд start и help в боте
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f"Приветствуем Вас! Для начала работы нажмите: /convert \n \
Увидеть список доступных валют: /values"
    bot.send_message(message.chat.id, text) #Отправка сообщения в бот

#Вывод доступных валют при вызове команды values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Список доступных валют: "
    # С помощью цикла перебираем весь словарь
    for i in key.keys():
        text = '\n'.join((text, i, ))
    bot.send_message(message.chat.id, text) #Отправка сообщения в бот

#Вывод доступных валют при вызове команды values
@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = "Выберите валюту, из которой конвертировать: "
    bot.send_message(message.chat.id, text, reply_markup=create_markup()) #Отправка сообщения с помощью клавиатуры
    bot.register_next_step_handler(message, base_handler) #Регистрируем обработчик для следующего шага

def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = "Выберите валюту, в которую конвертировать: "
    bot.send_message(message.chat.id, text, reply_markup=create_markup(base)) #Отправка сообщения c помощью клавиатуры, исключая уже выбранную валюту
    bot.register_next_step_handler(message, quote_handler, base) #Регистрируем обработчик для следующего шага

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = "Введите количество конвертируемой валюты: "
    bot.send_message(message.chat.id, text) #Отправка сообщения в бот
    bot.register_next_step_handler(message, amount_handler, base, quote) #Регистрируем обработчик для следующего шага

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    text = "Введите количество конвертируемой валюты: "
    try:
        answer = Convertor.get_price(base, quote, amount)
    # Вывод исключения для пользователя, если есть ошибка в команде
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка в команде:\n{e}")
    # Обрабатываем неизвестные ошибки из traceback и выводим пользователю
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.send_message(message.chat.id, f"Неизвестная ошибка:\n{e}")
    else:
        bot.send_message(message.chat.id, answer)

    bot.send_message(message.chat.id, f'Для повторной конвертации нажмите /convert \nСписок доступных валют: /values') #Отправка сообщения в бот

# Функция при вводе данных в строку пользователем

# #Функция для конвертации валюты
# @bot.message_handler(content_types=['text'])
# def converter(message: telebot.types.Message):
#     # Получаем данные из введенного пользователем текста, разделив его
#     values = message.text.split()
#     try:
#         # Проверка количества введенных параметров, если в списке не 3 элемента - выводим исключение
#         if len(values) != 3:
#             raise APIException('Неверное количество параметров!')
#         # Создаем объект от класса Convertor с введенными пользователем параметрами
#         answer = Convertor.get_price(*values)
#     # Вывод исключения для пользователя, если есть ошибка в команде
#     except APIException as e:
#         bot.send_message(message.chat.id, f"Ошибка в команде:\n{e}")
#     # Обрабатываем неизвестные ошибки из traceback и выводим пользователю
#     except Exception as e:
#         traceback.print_tb(e.__traceback__)
#         bot.send_message(message.chat.id, f"Неизвестная ошибка:\n{e}")
#     else:
#         bot.send_message(message.chat.id, answer)

bot.polling()

