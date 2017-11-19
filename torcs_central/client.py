from websocket import create_connection
import time
import json
import traceback
# ws = create_connection("ws://echo.websocket.org/")
# ws = create_connection("ws://130.215.219.68:9090/ws")
# print("Sending 'Hello, World'...")
# ws.send("Hello, World")
# print("Sent")
# print("Receiving...")
# result =  ws.recv()
# print("Received '%s'" % result)
# ws.close()

class wsClient():
    def __init__(self):
        self.configfilePath = "./config.json"
        self.config = json.load(open(self.configfilePath))
        self.ip = self.config['ip']
        self.port=self.config['port']
        self.ws = create_connection("ws://{}:{}/ws".format(self.ip,self.port))

    def testServer(self):
        print("Sending 'Hello, World'...")
        self.ws.send("Hello, World")
        print("Sent")
        print("Receiving...")
        result =  self.ws.recv()
        print("Received '%s'" % result)

    def sendMessage(self,msg):
        # msg = json.dumps(msg)
        try:
            self.ws.send(msg)
            result =  self.ws.recv()
            p=json.loads(result)
            k=json.loads(p)
            print(p,type(p))
            print(k,type(k),k['data'])
            # print(">>",json.loads(result)['data'])
            # print("Received '%s'" % result)
        except Exception as e:
            traceback.print_exc(e)
            print("Something went wrong while sending data")

    def closeConnection(self):
        self.ws.close()

if __name__ == '__main__':
    torcs_client = wsClient()
    torcs_client.testServer()
    for i in range(10):
        myjson = json.dumps({"data":i})
        torcs_client.sendMessage(myjson)
        print(i)
        time.sleep(0.5)
    torcs_client.closeConnection()        