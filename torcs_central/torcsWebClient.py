import requests
import json
import time
import os


class torcsWebClient():
    def __init__(self,configPath="./config.json"):
        self.config = json.load(open(configPath))
        self.ip=self.config['ip']
        self.port=self.config['port']
        self.clientID=self.config['clientID']
        self.url = "http://{}:{}/".format(self.ip,self.port)
        self.pulledModels = self.config['pulledModels']

    def pushData(self,Data):
        jsonData={"cmd":"updateResource",
                    "clientID":self.clientID}
        jsonData.update({"data":Data})
        files = {"actor":open('./models/actor.h5','rb'),"critic":open('./models/critic.h5','rb')}
        r = requests.post(self.url+'upload', files=files)
        r = requests.post(self.url, json=jsonData)
        r.json()

    def pullData(self):
        jsonData={"cmd":"fetchResource",
                    "clientID":self.clientID,
                    "data":{}
                    }
        
        if not os.path.isdir(self.pulledModels):
            os.mkdir(self.pulledModels)
            print("Directory created at ",self.pulledModels)

        r = requests.get('http://{}:{}/download/?file=actor'.format(self.ip,self.port))
        with open(os.path.join(self.pulledModels,'actor.h5'), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        r = requests.get('http://{}:{}/download/?file=critic'.format(self.ip,self.port))
        with open(os.path.join(self.pulledModels,'critic.h5'), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

 
        
        r = requests.post(self.url, json=jsonData)
        # r.json()
        return r.json()['data']

    def pingServer(self):
        jsonData = {"cmd":"ping","clientID":self.clientID,"data":{}}  
        r = requests.post(self.url, json=jsonData)
        print(r.json())
        if r.json()['status']==0:
            return True
        else:
            return False

if __name__ == '__main__':
    t_client = torcsWebClient(configPath="./config.json")
    for i in range(10):
        payload = {"cmd":"updateResource",
                    "clientID":t_client.clientID,
                    "data":{'value': i}
                    }
        # payload_f = {"cmd":"fetchResource",
        #           "clientID":t_client.clientID,
        #           "data":{'value': i}
        #           }
        print(t_client.pingServer())
        t_client.pushData(payload)
        t_client.pullData()
        time.sleep(2)   