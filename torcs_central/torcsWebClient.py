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

	def pushData(self,Data):
		jsonData={"cmd":"updateResource",
					"clientID":self.clientID}
		jsonData.update({"data":Data})
		r = requests.post(self.url, json=jsonData)
		print(r.json())

	def pullData(self):
		jsonData={"cmd":"fetchResource",
					"clientID":self.clientID,
					"data":{}
					}
		r = requests.post(self.url, json=jsonData)
		print(r.json())
		return r.json()['data']

	def pingServer(self):
		jsonData = {"cmd":"ping","clientID":self.clientID}	
		r = requests.post(self.url, json=jsonData)
		print(r.json())
		if r.json()['status']==0:
			return True
		else:
			return False

if __name__ == '__main__':
	t_client = torcsWebClient()
	for i in range(10):
		payload = {"cmd":"updateResource",
					"clientID":t_client.clientID,
					"data":{'value': i}
					}
		# payload_f = {"cmd":"fetchResource",
		# 			"clientID":t_client.clientID,
		# 			"data":{'value': i}
		# 			}
		print(t_client.pingServer())
		t_client.pushData(payload)
		t_client.pullData()
		time.sleep(2)	