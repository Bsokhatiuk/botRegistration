from datetime import datetime
def generate_weekly_schedule_template(date_list):
    # Розбиваємо рядок на список дат
    dates = date_list.split(',')

    # Створюємо порожній словник для зберігання шаблону графіку по тижнях
    weekly_schedule_template = {}

    # Поточний індекс тижня
    current_week = 1

    # Створюємо шаблон для поточного тижня
    current_week_template = {'Mo': 0, 'Tu': 0, 'We': 0, 'Th': 0, 'Fr': 0, 'Sa': 0, 'Su': 0}
        # Проходимо по списку дат
    list_dates = []
    for date_str in dates:
        # Перетворюємо рядок у форматі "YYYY-MM-DD" на об'єкт datetime
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        list_dates.append(date_obj)
    list_dates.sort()
    # Проходимо по списку дат
    day_of_week_priv = -1
    for date_obj in list_dates:
        day_of_week = date_obj.weekday()
        if day_of_week < day_of_week_priv:
            weekly_schedule_template[current_week] = current_week_template
            current_week_template = {'Mo': 0, 'Tu': 0, 'We': 0, 'Th': 0, 'Fr': 0, 'Sa': 0, 'Su': 0}
            current_week += 1
        day_of_week_priv = day_of_week
        # Оновлюємо значення шаблону для відповідного дня тижня
        if day_of_week == 0:
            current_week_template['Mo'] = 1
        elif day_of_week == 1:
            current_week_template['Tu'] = 1
        elif day_of_week == 2:
            current_week_template['We'] = 1
        elif day_of_week == 3:
            current_week_template['Th'] = 1
        elif day_of_week == 4:
            current_week_template['Fr'] = 1
        elif day_of_week == 5:
            current_week_template['Sa'] = 1
        elif day_of_week == 6:
            current_week_template['Su'] = 1

    weekly_schedule_template[current_week] = current_week_template
    return weekly_schedule_template, list_dates[0].strftime('%Y-%m-%d')


from datetime import datetime, timedelta


def generate_schedule(template, start_date, current_date):
    days_passed = (current_date - start_date).days
    week_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    template_keys = list(template.keys())
    current_week = template_keys[(days_passed // 7) % len(template_keys)]
    shift_template = template[current_week]
    schedule_for_day = shift_template[week_days[current_date.weekday()]]
    return bool(schedule_for_day)



def get_format_date(date_string):
    uk_day_names = {
        0: 'Пн',
        1: 'Вт',
        2: 'Ср',
        3: 'Чт',
        4: 'Пт',
        5: 'Сб',
        6: 'Нд'
    }
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    day_name = uk_day_names[date_object.weekday()]
    if date_object.month < 10:
        month_name = '0' + str(date_object.month)
    else:
        month_name = str(date_object.month)
    formatted_date = f'{day_name} {date_object.day:02d}.{month_name}'
    return formatted_date


class Schedule:
    def __init__(self, template, start_date, start_time, end_time, cnt_works,
                 template_two=None, start_date_two=None, start_time_two=None, end_time_two=None, holidays=[], seekdays=[]):
        self.template = template
        self.start_date = start_date
        self.start_time = start_time
        self.end_time = end_time
        self.cnt_works = cnt_works
        self.template_two = template_two
        self.start_date_two = start_date_two
        self.start_time_two = start_time_two
        self.end_time_two = end_time_two
        self.holidays = holidays
        self.seekdays = seekdays

    def generate_schedule(self, list_days, list_records):
        pass
class Record:
    def __init__(self, user_id, user_name, user_phone, comment, phone_employee, service,
                 cr_date, book_datetime, status):
        self.user_id = user_id
        self.user_name = user_name
        self.user_phone = user_phone
        self.comment = comment
        self.phone_employee = phone_employee
        self.service = service
        self.cr_date = cr_date
        self.book_datetime = book_datetime
        self.status = status

class Service():
    def __init__(self, name, price, duration):
        self.price = price
        self.name = name
        self.duration = duration