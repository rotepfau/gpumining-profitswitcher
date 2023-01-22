from time import sleep, ctime, time
import json
from requests import request, exceptions
import os
import tomllib
from sys import platform
import sqlite3

with open('config.toml' if not platform.__contains__('linux') else '/home/user/gpumining-profitswitcher/config.toml', 'rb') as config_file:
    config = tomllib.load(config_file)


class Hive(object):

    def __init__(self, token):
        self.token = token
        self.farm_id = self.__get_farm_id_by_name(config['FARM_NAME'])
        self.worker_id = self.__get_worker_id_by_name(config['WORKER_NAME'])

    def api_query(self, method, command, payload=None, params=None):
        if payload is None:
            payload = {}
        if params is None:
            params = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }

        while True:
            try:
                s = request(method, 'https://api2.hiveos.farm/api/v2' + command, data=payload, params=params,
                            headers=headers, timeout=100)
            except exceptions.ConnectionError:
                print('Oops. Connection failed to HiveOs')
                sleep(15)
                continue
            except exceptions.Timeout:
                print('Oops. Timed out waiting for a response from HiveOs')
                sleep(15)
                continue
            except exceptions.TooManyRedirects:
                print('Oops. Exceeded number of requests from HiveOs, Wait 30 minutes')
                sleep(1800)
                continue
            else:
                print(s.status_code)
                api = s.json()
                break

        return api

    def __get_farms(self):
        return self.api_query('GET', '/farms')

    def __get_farm_id_by_name(self, name: str) -> int:
        print('Getting farm id by name')
        farms = self.__get_farms()['data']
        return next(farm for farm in farms if farm['name'] == name)['id']

    def __get_worker_id_by_name(self, name: str) -> int:
        print('Getting worker id by name')
        workers = self.__get_workers_preview()['data']
        return next(worker for worker in workers if worker['name'] == name)['id']

    def __get_workers_preview(self) -> dict:
        return self.api_query('GET', f'/farms/{self.farm_id}/workers/preview')

    def get_current_fs(self) -> str:
        return self.api_query('GET', f'/farms/{self.farm_id}/workers/{self.worker_id}')['flight_sheet']['name']

    def set_current_fs(self, id: int):
        fs = {'fs_id': id}
        fs_json = json.dumps(fs)
        self.api_query(
            'PATCH', f'/farms/{self.farm_id}/workers/{self.worker_id}', payload=fs_json)

    def get_all_fs(self) -> dict:
        return self.api_query('GET', f'/farms/{self.farm_id}/fs')['data']


class Whattomine(object):
    def __init__(self, url) -> None:
        self.url = url
        pass

    def get_most_profitable_coin(self) -> str:
        print('Getting whattomine data')
        req = request('GET', self.url, timeout=100)
        to_json = req.json()
        coins = to_json['coins']
        most_profitable_coin = next(
            coin for coin in coins if coin in config['COINS'])
        print(f'Most profitable coin: {most_profitable_coin}')
        return most_profitable_coin


def set_database(coin: str):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY, date INTEGER, coin TEXT)')
    cur.execute('INSERT INTO data(date, coin) VALUES(?, ?)',
                (int(time()), coin))
    con.commit()
    con.close()


def main():
    print(ctime(time()))
    cHive = Hive(config['HIVE_API_KEY'])
    cWhattomine = Whattomine(config['WHATTOMINE_JSON'])
    most_profitable_coin = cWhattomine.get_most_profitable_coin()
    current_fs = cHive.get_current_fs()
    if current_fs not in config['COINS']:
        if platform.__contains__('linux'):
            set_database('NULL')
            os.system(
                'message danger "Current flight sheet is not named properly. It should be the same as coins"')
        raise Exception(
            'Current flight sheet is not named properly. It should be the same as coins')
    if current_fs == most_profitable_coin:
        if platform.__contains__('linux'):
            set_database(most_profitable_coin)
            os.system(f'message info "{most_profitable_coin}"')
        return print('Current flight sheet is already the most profitable coin. Exiting')
    all_fs = cHive.get_all_fs()
    if not any(fs['name'] == most_profitable_coin for fs in all_fs):
        if platform.__contains__('linux'):
            set_database('NULL')
            os.system(
                'message danger "Most profitable coin not configured. Exiting"')
        return print('Most profitable coin not configured. Exiting')
    new_fs = [fs for fs in all_fs if fs.get(
        'name') == most_profitable_coin][0]
    cHive.set_current_fs(new_fs['id'])
    if platform.__contains__('linux'):
        set_database(most_profitable_coin)
        os.system(f'message success "{new_fs["name"]}"')
    print(f'New flight sheet {new_fs["name"]}')
    print('Done')


if __name__ == '__main__':
    main()
