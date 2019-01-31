# -*- coding: utf-8 -*-

from datetime import datetime

# Формирование массива данных
with open('weather2018.csv', 'r', encoding='UTF-8') as f:
    weather_stat = {}
    for line in f:
        if not line.startswith('#'):
            row = line.replace('\n', '')[1:-2]
            if row.count('";"') == 28:
                cols = row.split('";"')
                dt = cols[0].split()[0]
                temp = float(cols[1])
                if cols[23].replace('.', '').isdigit():
                    rainy = float(cols[23])
                elif cols[23] == 'Следы осадков':
                    rainy = 0.01
                else:
                    rainy = 0
                if dt in weather_stat:
                    curr_temp_sum, curr_temp_cnt, curr_rainy_sum = weather_stat[dt]
                    curr_temp_sum += temp
                    curr_temp_cnt += 1
                    curr_rainy_sum += rainy
                    weather_stat[dt] = (curr_temp_sum, curr_temp_cnt, curr_rainy_sum)
                else:
                    weather_stat[dt] = (temp, 1, rainy)

# Сортировка дат в порядке возрастания
# for dt in weather_stat.keys():
#     day, month, year = dt.split('.')

# Вычисление усредненных данных по дням
for dt in weather_stat.keys():
    temp_sum, temp_cnt, rainy_sum = weather_stat[dt]
    avg_temp = round(temp_sum / temp_cnt, 1)
    weather_stat[dt] = (avg_temp, rainy_sum)

# Вычисление средней, максимальной, минимальной температуры
# и максимального количества осадков по периоду
cnt_rainy = 0
max_temp, min_temp, max_rainy = -100, 100, 0
max_temp_date = ''
min_temp_date = ''
max_rainy_date = ''
mean_temp_sum = 0
mean_cnt = 0

for dt, (avg_temp, rainy_sum) in weather_stat.items():
    mean_temp_sum += avg_temp
    mean_cnt += 1
    if max_temp < avg_temp:
        max_temp = avg_temp
        max_temp_date = dt
    if min_temp > avg_temp:
        min_temp = avg_temp
        min_temp_date = dt
    if rainy_sum > 0:
        cnt_rainy += 1
    if max_rainy < rainy_sum:
        max_rainy = rainy_sum
        max_rainy_date = dt

mean_temp = round(mean_temp_sum / mean_cnt, 1)

# ## Вывод информации
print(f'{"Средняя температура по дням":^34}\n')
print(f' {"Дата":10} {"t":>4}\u00B0 {"Кол-во осадков":>15} ')
rev_keys = reversed(list(weather_stat.keys()))
for dt in rev_keys:
    temp, rainy = weather_stat[dt][0], weather_stat[dt][1]
    print(f'|{dt}|{float(temp):>5.1f}|{float(rainy):>15.2f}|')

# print('')
print(f'{"Средняя температура за период:":>37} {mean_temp:+}')
print(f'{"Максимальная температура за период:":>37} {max_temp:+}')
print(f'{"Минимальная температура за период:":>37} {min_temp:+}')
print(f'{"Самый теплый день:":>37} {max_temp_date} (t\u00B0 = {max_temp:+})')
print(f'{"Самый холодный день:":>37} {min_temp_date} (t\u00B0 = {min_temp:+})')
print(f'{"Самый дождливый день:":>37} {max_rainy_date} (Кол-во осадков, мм = {max_rainy})')
print(f'{"Дождливых дней за период:":>37} {cnt_rainy} дн.')
