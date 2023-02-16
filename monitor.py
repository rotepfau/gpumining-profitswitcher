import sqlite3
from os import system
from sys import argv
from time import time


def get_timeframe():
    now = int(time())
    if len(argv) != 2 or type(argv[1]) != int:
        print('Timeframe not selected, using all values from table')
        return (0, )
    days_selected = int(argv[1]) * 60 * 60 * 24
    return (now - days_selected, )


def calculate_percents(rows_array):
    statistic = dict()
    for i, data in enumerate(rows_array[:-1]):
        timelength = rows_array[i + 1][1] - data[1]
        if data[2] not in statistic:
            statistic[data[2]] = 0
        statistic[data[2]] += timelength

    totaltime = 0
    for timestamp in statistic.values():
        totaltime += timestamp

    percentvalue = int(time())
    if len(argv) == 2:
        percentvalue = argv[1]
    percenttime = f'{percentvalue} day(s)\n'
    for coin, timestamp in statistic.items():
        percent = timestamp / totaltime * 100
        percenttime += f'{int(percent)}% {coin} \n'
    system(f'message warning "{percenttime}"')


if __name__ == '__main__':
    con = sqlite3.connect('/home/user/gpumining-profitswitcher/database.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM data WHERE date >= ?',
                      (get_timeframe())).fetchall()
    calculate_percents(res)
