import requests
import json
import time


class torcsWebClient():
	def __init__(self):
		self.config = json.load(open("./config.json"))
		self.ip=self.config['ip']
		self.port=self.config['port']
		self.clientID=self.config['clientID']
		self.url = "http://{}:{}/".format(self.ip,self.port)

	def pushData(self,jsonData):
		r = requests.post(self.url, json=jsonData)
		print(r.text)

if __name__ == '__main__':
	t_client = torcsWebClient()
	for i in range(10):
		payload = {"clientID":t_client.clientID,
					"data":{'value': i}
					}
		t_client.pushData(payload)
		time.sleep(2)	