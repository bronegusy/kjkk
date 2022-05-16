import telebot
import psycopg2
from telebot import types

token = '5025079835:AAFmJDR_eWLl2XKKhSkzJnLmfFRfZ187gM0'
bot = telebot.TeleBot(token)
print('Bot is running')

try:
    connection = psycopg2.connect(database="school_timetable",
                                user="postgres",
                                password="1111",
                                host="localhost",
                                port="5432")
    cursor = connection.cursor()
    print("Database connection working")
except:
    print("Database connection failed")

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row('Понедельник')
    keyboard.row('Вторник')
    keyboard.row('Среда')
    keyboard.row('Четверг')
    keyboard.row('Пятница')
    bot.send_message(message.chat.id, 'Привет! Я подскажу тебе расписание!', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_timetable(message):
    if message.text == 'Понедельник':
        cursor.execute("""SELECT timetable.timetable.*, timetable.teacher.full_name
                        FROM timetable.timetable, timetable.teacher
                        WHERE timetable.timetable.day='Понедельник' AND
                        timetable.timetable.subject = timetable.teacher.subject
                        ORDER BY timetable.timetable.start_time;""")
        records = list(cursor.fetchall())
        timetable = ""
        for i in range(len(records)):
            timetable += 'Начало: ' + str(records[i][4]) + '. Кабинет: ' + str(records[i][3]) + '. Урок:  ' +  str(records[i][2]) + ". Учитель: " + str(records[i][5]) + "\n"
        print(timetable)
        bot.send_message(message.chat.id, "Расписание на понедельник:")
        bot.send_message(message.chat.id, timetable)
    elif message.text == 'Вторник':
        bot.send_message(message.chat.id, "Расписание на вторник:")
    elif message.text == 'Среда':
        bot.send_message(message.chat.id, "Расписание на среду:")
    elif message.text == 'Четверг':
        bot.send_message(message.chat.id, "Расписание на четверг:")
    elif message.text == 'Пятница':
        bot.send_message(message.chat.id, "Расписание на пятницу:")

bot.infinity_polling()