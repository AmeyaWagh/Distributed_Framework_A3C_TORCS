import requests
import json

config = json.load(open("./config.json"))

ip=config['ip']
port=config['port']
clientID=config['clientID']

payload = {"clientID":clientID,
			"data":{'key1': 'value1', 
					'key2': 'value2'}
		}

r = requests.post("http://localhost:9090/", json=payload)
print(r.text)