import sqlite3

if __name__ == '__main__':
    statistic = dict()
    con = sqlite3.connect('/home/user/gpumining-profitswitcher/database.db')
    cur = con.cursor()
    res = cur.execute('select * from data').fetchall()
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
