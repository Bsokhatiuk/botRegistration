import datetime
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
    return weekly_schedule_template