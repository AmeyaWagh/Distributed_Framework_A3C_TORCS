from websocket import create_connection
import time
import json
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
        msg = json.dumps(msg)
        try:
            self.ws.send(msg)
        except:
            print("Something went wrong")

    def closeConnection(self):
        self.ws.close()

if __name__ == '__main__':
    torcs_client = wsClient()
    torcs_client.testServer()
    for i in range(10):
        torcs_client.sendMessage(str(i))
        print(i)
        time.sleep(0.5)
    torcs_client.closeConnection()        