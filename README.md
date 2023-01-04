### **ABOUT**

This script is intend to use on the same machine's rig, but you can launch on another\* machine with a small functionallity loss.

\*Right now it only support windows as "another" machine

\*\*Tested with python 3.11.1

### **_PRE_-INSTALLATION**

1. Go to [WhatToMine](https://whattomine.com), setup all algos and parameters, _calculate_ it, press _JSON_ button on top right page and then copy URL from the page that you got redirected. Paste it somewhere as we will use it later on installation phase
2. On [hiveos](https://the.hiveos.farm), create every _flight sheet_ you want and nameit _exactly_ how the coin is named on WhatToMine i.e EthereumClassic
3. Still on hiveos, setup all overclock settings and toggle on _Auto Select Algo_ option

### **INSTALLATION**

Preferable on the rig machine. You can either start a remote access hive shell or by local console

1. Go to home directory<br>
   `cd ~`
2. Clone this repo<br>
   `git clone https://github.com/rotepfau/gpumining-profitswitcher.git`<br>
3. Copy _example.config.toml_, rename it to _config.toml_ and replace all items to yours configuration ie:<br>
   `HIVE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3MTEwZTIyMi02ZGM2LTQ4MmYtOGE1OS0wOTcwYmQ2NjdkZGQifQ.eyJleHAiOjE5ODY0NzkzMzYyMjQsIm5iZiI6MTY3MDg2MDEzNjIyNCwiaWF0IjoxNjcwODYwMTM2MjI0LCJqdGkiOiI2Y2Q5NDQ2Yy00OTdmLTRmOWEtYmUwNC01MGUwODhmZGYyNjQiLCJzdWIiOiI2Y2Q5NDQ2Yy00OTdmLTRmOWEtYmUwNC01MGUwODhmZGYyNjQifQ.UXsnsMXQrLogZQwcPuG_QHZtsxi9j0Jvrv_ZI0k_rzw"`<br> \*[Hive](hiveon.com) api key can be generated on accounts/sessions<br>
   `FARM_NAME = "Joe's Farm"`<br>
   `WORKER_NAME = "RIG01"`<br>
   `COINS = ["Aeternity","Aion","Alephium","Beam","BitcoinGold","Ergo","EthereumClassic","Flux","Kaspa","Ravencoin","Zano"]`<br>
   `WHATTOMINE_JSON = "https://whattomine.com/coins.json?eth=true&factor%5Beth_hr%5D=116.0&factor%5Beth_p%5D=360.0&e4g=true&factor%5Be4g_hr%5D=132.0&factor%5Be4g_p%5D=360.0&zh=true&factor%5Bzh_hr%5D=132.0&factor%5Bzh_p%5D=320.0&cnh=true&factor%5Bcnh_hr%5D=2600.0&factor%5Bcnh_p%5D=360.0&cng=true&factor%5Bcng_hr%5D=4600.0&factor%5Bcng_p%5D=360.0&s5r=true&factor%5Bs5r_hr%5D=1.12&factor%5Bs5r_p%5D=240.0&factor%5Bcx_hr%5D=0.0&factor%5Bcx_p%5D=0.0&eqa=true&factor%5Beqa_hr%5D=624.0&factor%5Beqa_p%5D=320.0&cc=true&factor%5Bcc_hr%5D=17.2&factor%5Bcc_p%5D=320.0&cr29=true&factor%5Bcr29_hr%5D=17.2&factor%5Bcr29_p%5D=360.0&hh=true&factor%5Bhh_hr%5D=1180.0&factor%5Bhh_p%5D=320.0&ct32=true&factor%5Bct32_hr%5D=1.0&factor%5Bct32_p%5D=320.0&eqb=true&factor%5Beqb_hr%5D=44.0&factor%5Beqb_p%5D=320.0&b3=true&factor%5Bb3_hr%5D=2.56&factor%5Bb3_p%5D=320.0&factor%5Bns_hr%5D=0.0&factor%5Bns_p%5D=0.0&al=true&factor%5Bal_hr%5D=230.0&factor%5Bal_p%5D=360.0&factor%5Bops_hr%5D=0.0&factor%5Bops_p%5D=0.0&eqz=true&factor%5Beqz_hr%5D=78.0&factor%5Beqz_p%5D=360.0&zlh=true&factor%5Bzlh_hr%5D=104.0&factor%5Bzlh_p%5D=320.0&kpw=true&factor%5Bkpw_hr%5D=42.4&factor%5Bkpw_p%5D=320.0&ppw=true&factor%5Bppw_hr%5D=42.4&factor%5Bppw_p%5D=320.0&x25x=true&factor%5Bx25x_hr%5D=11.6&factor%5Bx25x_p%5D=360.0&fpw=true&factor%5Bfpw_hr%5D=40.0&factor%5Bfpw_p%5D=360.0&vh=true&factor%5Bvh_hr%5D=1.84&factor%5Bvh_p%5D=360.0&factor%5Bcost%5D=0.0&factor%5Bcost_currency%5D=USD&sort=Revenue&volume=0&revenue=24h&factor%5Bexchanges%5D%5B%5D=&factor%5Bexchanges%5D%5B%5D=binance&factor%5Bexchanges%5D%5B%5D=bitfinex&factor%5Bexchanges%5D%5B%5D=bitforex&factor%5Bexchanges%5D%5B%5D=bittrex&factor%5Bexchanges%5D%5B%5D=coinex&factor%5Bexchanges%5D%5B%5D=exmo&factor%5Bexchanges%5D%5B%5D=gate&factor%5Bexchanges%5D%5B%5D=graviex&factor%5Bexchanges%5D%5B%5D=hitbtc&factor%5Bexchanges%5D%5B%5D=ogre&factor%5Bexchanges%5D%5B%5D=poloniex&factor%5Bexchanges%5D%5B%5D=stex&dataset=Main"`<br>
   \*This is the WhatToMine url that you side noted on pre-installation phase
4. Create [python virtual environment](https://docs.python.org/3/library/venv.html) and activate it
5. Install dependencies<br>
   `pip install -r requirements.txt`
6. Edit crontab file to keep script running every hour<br>
   `vi /hive/etc/crontab.root`<br>
   or<br>
   `nano /hive/etc/crontab.root`
7. Add this to the end of file<br>
   `0 * * * * /home/user/gpumining-profitswitcher/.venv/bin/python /home/user/gpumining-profitswitcher/core.py &>> /home/user/crontab-profitswitcher.log`<br>
   \*Keep blank line on very last line of the file or will not work
   \*\*If you wanna to change script interval take a look on [crontab-generator](https://crontab-generator.com)
8. Reboot to crontab chage take effect

### **DISCLAIMER**

I develop just as a hobby, wondering if that could change on upcoming days. Contributions are very welcome, specially on this README (feel free to correct my BAD english).

### **TODO**

1. Take some screenshots
2. Add some comments to be easier to new contributors
