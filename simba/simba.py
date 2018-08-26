import requests
from utils.log import __console

class Simba:
    def __init__(self):
        r = requests.get("http://172.31.16.165:5000/initiatecall")
        __console.log( r )
        self.call_id = r.json['callId']
        self.initialResponse = r.json['message']

    def getInitiateResponse(self):
        r = requests.get("http://172.31.16.165:5000/initiatecall")
        return r.text
    
    def send_message(self, message):
        payload = {'message': message, 'callId': self.call_id}
        r = requests.get("http://172.31.16.165:5000/sendMessage", params=payload)
        return r.text

    def get_initiate_message(self):
        return self.initialResponse

        

