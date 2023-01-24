import sqlite3
import sys
from time import time


def get_timeframe():
    if len(sys.argv) != 2:
        raise Exception('Missed timeframe parameter in days')
    now = int(time())
    days_selected = int(sys.argv[1]) * 60 * 60 * 24
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

    for coin, timestamp in statistic.items():
        percent = timestamp / totaltime * 100
        print(coin, int(percent))


if __name__ == '__main__':
    con = sqlite3.connect('/home/user/gpumining-profitswitcher/database.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM data WHERE date >= ?',
                      (get_timeframe())).fetchall()
    calculate_percents(res)
