# -*- coding: utf-8 -*-

from datetime import datetime

## Формирование массива данных
f = open('weather2018.csv', 'r', encoding='UTF-8')
weather_stat = []
for line in f:
    if not line.startswith('#'):
        row = line.replace('\n', '')[1:-2]
        if row.count('";"') == 28:
            cols = row.split('";"')
            dt = datetime.strptime(cols[0].split()[0], '%d.%m.%Y').date()
            temp = float(cols[1])
            rainy = cols[23]
            weather_stat.append((dt, temp, rainy))
f.close()

## Формирование сортированного списка дат
dates = sorted({str[0] for str in weather_stat})

## Формирование усредненных данных по дням
mean_stats_daily = []
mean_temp_sum = 0

for dt in dates:
    cnt, sum_temp, sum_rain = 0, 0, 0
    for stat in weather_stat:
        if stat[0] == dt:
            cnt += 1
            sum_temp += stat[1]
            if stat[2].replace('.', '').isdigit():
                sum_rain += float(stat[2])
            elif stat[2] == 'Следы осадков':
                sum_rain += 0.01
    mean_temp = round(sum_temp / cnt, 1)
    mean_temp_sum += mean_temp
    mean_stats_daily.append((dt, mean_temp, float(sum_rain)))

## Вычисление средней, максимальной, минимальной температуры
## и максимального количества осадков по периоду
mean_temp_whole = round(mean_temp_sum / len(mean_stats_daily), 1)

max_date, max_temp = mean_stats_daily[0][0:2]
min_date, min_temp = mean_stats_daily[0][0:2]
max_rainy_date, max_rainy = mean_stats_daily[0][0::2]

for stat in mean_stats_daily:
    if max_temp < stat[1]:
        max_temp = stat[1]
        max_date = stat[0]
    if min_temp > stat[1]:
        min_temp = stat[1]
        min_date = stat[0]
    if max_rainy < stat[2]:
        max_rainy = stat[2]
        max_rainy_date = stat[0]

## Подсчет количесва дождливых дней
rainy_days = len([stat for stat in mean_stats_daily if stat[2] > 0])

## Вывод информации
print(f'{"Средняя температура по дням":^34}\n')
print(f' {"Дата":10} {"t":>4}\u00B0 {"Кол-во осадков":>15} ')
for dt in dates:
    for stat in mean_stats_daily:
        if stat[0] == dt:
            print(f'|{stat[0]}|{stat[1]:>5}|{stat[2]:>15}|')

print('')
print(f'{"Средняя температура за период:":>37} {mean_temp_whole}')
print(f'{"Максимальная температура за период:":>37} {max_temp}')
print(f'{"Минимальная температура за период:":>37} {min_temp}')
print(f'{"Самый теплый день:":>37} {max_date} (t\u00B0 = {max_temp})')
print(f'{"Самый холодный день:":>37} {min_date} (t\u00B0 = {min_temp})')
print(f'{"Самый дождливый день:":>37} {max_rainy_date} (Кол-во осадков, мм = {max_rainy})')
print(f'{"Дождливых дней за период:":>37} {rainy_days} дн.')
