import telebot
import webbrowser
from telebot import types
import sqlite3




bot = telebot.TeleBot("6261304132:AAHpLOESBONB8dn8IVcvTjPI1US01zujwFE")
free_slots = []

# @bot.message_handler(commands=['init_db'])
# def main(message):
#     conn = sqlite3.connect('botregister.sqlite3')
#     cur = conn.cursor()
#     cur.execute('CREATE TABLE IF NOT EXISTS users (id int primary key, name varchar(50), pass varchar(50))')
#     conn.commit()
#     cur.close()
#     conn.close()
#     bot.send_message(message.chat.id, 'Зараз тебе зареєструємо')
#     bot.register_next_step_handler(message, user_name)

def user_name():
    pass

@bot.message_handler(commands=['user_info'])
def main(massege):
    bot.send_message(massege.chat.id, massege)

@bot.message_handler(commands=['site'])
def site(massege):
    webbrowser.open('https://www.vodafone.ua/')


# Dictionary to store the appointments schedule
schedule = {}


@bot.message_handler(commands=['book'])
def book_appointment(message):
    markup = types.InlineKeyboardMarkup()
    for day in schedule.keys():
        button = types.InlineKeyboardButton(text=day, callback_data='day_' + day)
        markup.add(button)

    if markup.keyboard:
        bot.send_message(message.chat.id, "Select a day to book an appointment:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "No available days for appointments.")


# Function to view available slots
@bot.message_handler(commands=['view'])
def view_appointments(message):
    available_slots = [slot for slot, is_available in schedule.items() if is_available]

    if available_slots:
        bot.send_message(message.chat.id, "Available appointment slots: " + ', '.join(available_slots))
    else:
        bot.send_message(message.chat.id, "No available slots at the moment.")


# Function to view the doctor's schedule
@bot.message_handler(commands=['schedule'])
def view_schedule(message):
    schedule_text = "Doctor's Schedule:\n"
    for day, slots in schedule.items():
        schedule_text += day + ":\n"
        for slot, is_available in slots.items():
            status = "Available" if is_available else "Occupied"
            schedule_text += slot + " - " + status + "\n"
        schedule_text += "\n"

    bot.send_message(message.chat.id, schedule_text)

# Обробник відповіді на InlineKeyboardButton для вибору дня
@bot.callback_query_handler(func=lambda call: call.data.startswith('day_'))
def select_day(call):
    selected_day = call.data.split('_')[1]

    if selected_day in schedule:
        available_slots = [slot for slot, is_available in schedule[selected_day].items() if is_available]

        if available_slots:
            markup = types.InlineKeyboardMarkup()
            for slot in available_slots:
                button = types.InlineKeyboardButton(text=slot, callback_data='slot_' + selected_day + '_' + slot)
                markup.add(button)

            bot.send_message(call.message.chat.id, "Select a time slot for " + selected_day + ":", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id,
                             "No available slots for " + selected_day + ". Please choose another day.")
    else:
        bot.send_message(call.message.chat.id, "Invalid day selection. Please try again.")


# Обробник відповіді на InlineKeyboardButton для вибору години
@bot.callback_query_handler(func=lambda call: call.data.startswith('slot_'))
def select_slot(call):
    selected_data = call.data.split('_')
    selected_day = selected_data[1]
    selected_slot = selected_data[2]

    if selected_day in schedule and selected_slot in schedule[selected_day] and schedule[selected_day][selected_slot]:
        schedule[selected_day][selected_slot] = False
        bot.send_message(call.message.chat.id,
                         "You have successfully booked an appointment on " + selected_day + " at " + selected_slot)
    else:
        bot.send_message(call.message.chat.id,
                         "The selected slot on " + selected_day + " is already occupied. Please choose another slot.")


# Set the initial schedule with all slots available
schedule = {
    "2023-06-21": {
        "09:00": True,
        "10:00": True,
        "11:00": True,
        "12:00": True,
        "13:00": True
    },
    "2023-06-22": {
        "09:00": True,
        "10:00": True,
        "11:00": True,
        "12:00": True,
        "13:00": True
    }
}


bot.polling(none_stop=True)



