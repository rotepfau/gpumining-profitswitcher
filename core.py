import os
from time import sleep
import json
from requests import request, exceptions
from dotenv import load_dotenv
load_dotenv()


class Hive(object):

    def __init__(self, token):
        self.token = token
        self.farm_id = self.__get_farm_id_by_name(os.environ.get("FARM_NAME"))
        self.worker_id = self.__get_worker_id_by_name(
            os.environ.get("WORKER_NAME"))

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
                print(s)
                api = s.json()
                break

        return api

    def __get_farms(self):
        return self.api_query('GET', '/farms')

    def __get_farm_id_by_name(self, name: str) -> int:
        print("Getting farm id by name")
        farms = self.__get_farms()["data"]
        return next(farm for farm in farms if farm["name"] == name)["id"]

    def __get_worker_id_by_name(self, name: str) -> int:
        print("Getting worker id by name")
        workers = self.__get_workers_preview()["data"]
        return next(worker for worker in workers if worker["name"] == name)["id"]

    def __get_workers_preview(self):
        return self.api_query("GET", f"/farms/{self.farm_id}/workers/preview")

    def get_current_fs(self) -> str:
        return self.api_query("GET", f"/farms/{self.farm_id}/workers/{self.worker_id}")["flight_sheet"]["name"]

    def set_current_fs(self, id: int):
        fs = {"fs_id": id}
        fs_json = json.dumps(fs)
        return self.api_query("PATCH", f'/farms/{self.farm_id}/workers/{self.worker_id}', payload=fs_json)

    def get_all_fs(self):
        return self.api_query("GET", f"/farms/{self.farm_id}/fs")["data"]


class Whattomine(object):
    def __init__(self, url) -> None:
        self.url = url
        pass

    def get_most_profitable_coin(self) -> str:
        print("Getting whattomine data")
        req = request("GET", self.url, timeout=100)
        to_json = req.json()
        coins = to_json["coins"]
        most_profitable_coin = next(
            coin for coin in coins if coin in os.environ.get("COINS"))
        print(f"Most profitable coin: {most_profitable_coin}")
        return most_profitable_coin


def main():
    cHive = Hive(os.environ.get("HIVE_API_KEY"))
    cWhattomine = Whattomine(os.environ.get("WHATTOMINE_URL"))
    most_profitable_coin = cWhattomine.get_most_profitable_coin()
    current_fs = cHive.get_current_fs()
    if current_fs not in os.environ.get("COINS"):
        raise Exception(
            "Current flight sheet is not named properly. It should be the same as coins")
    if current_fs == most_profitable_coin:
        return print("Current flight sheet is already the most profitable coin. Exiting")
    all_fs = cHive.get_all_fs()
    if not any(fs['name'] == most_profitable_coin for fs in all_fs):
        return print("Most profitable coin not configured. Exiting")
    new_fs_id = [fs for fs in all_fs if fs.get(
        'name') == most_profitable_coin][0]["id"]
    print("Setting up new flight sheet")
    print(cHive.set_current_fs(new_fs_id))
    print("Done.")


if __name__ == '__main__':
    main()
