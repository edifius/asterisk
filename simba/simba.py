import requests
from utils.log import __console

class Simba:
    def __init__(self):
        r = requests.get("http://172.31.16.165:5000/initiatecall")
        __console.log("This is the response!")
        __console.log(r)

