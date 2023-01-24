import sqlite3
import sys
from time import time


def getTimeFrame():
    if len(sys.argv) != 2:
        raise Exception('Missed timeframe parameter in days')
    now = int(time())
    days_selected = int(sys.argv[1]) * 60 * 60 * 24
    return str(now - days_selected)


if __name__ == '__main__':
    timeframe = getTimeFrame()
    statistic = dict()
    con = sqlite3.connect('/home/user/gpumining-profitswitcher/database.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM data WHERE date >= ?',
                      timeframe).fetchall()
    for i, data in enumerate(res[:-1]):
        timelength = res[i + 1][1] - data[1]
        if data[2] not in statistic:
            statistic[data[2]] = 0
        statistic[data[2]] += timelength

    totaltime = 0
    for timestamp in statistic.values():
        totaltime += timestamp

    for coin, timestamp in statistic.items():
        percent = timestamp / totaltime
        print(coin, percent)
