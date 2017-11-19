import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import datetime
import json
import os
config=json.load(open("./torcs_central/config.json"))
resourcePath=config['resourcePath']

if not os.path.isdir(resourcePath):
    os.mkdir(resourcePath)
    print("Directory created at ",resourcePath)

global resource
resource=[]
log=[]

def handlerequest(request):
    cmd=request['cmd']
    if cmd=='ping':
        return json.dumps({"response":"ping_success","status":0})
    elif cmd=='updateResource':
        return json.dumps({"response":"update_success","status":0})
    elif cmd=='fetchResource':
        return json.dumps({"response":"update_success","status":0,"data":resource})
    else:
        return request


class Upload(tornado.web.RequestHandler):
    def post(self):
        print(self.request.files['actor'][0].keys())
        print(self.request.files['critic'][0].keys())
        actor_body = self.request.files['actor'][0]['body']
        critic_body = self.request.files['critic'][0]['body']
        with open(os.path.join(resourcePath,'actor.h5'),'wb') as fp:
            fp.write(actor_body)
        with open(os.path.join(resourcePath,'critic.h5'),'wb') as fp:
            fp.write(critic_body)
        self.write(json.dumps({"response":"update_success","status":0}))    
        

class MyHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        print(data)
        global resource
        resource.append(data)
        try:
            log.append([data['clientID'],data['cmd'],datetime.datetime.now().isoformat()])
        except:
            print("no clientID")
        self.write(handlerequest(data))

    def get(self):
        # items = ["Item 1", "Item 2", "Item 3"]
        # if resource is not None:
        #     items = [[elem['clientID'],elem['cmd']] for elem in resource]
        # else:
        #     items = []
        items=log
        self.render("index.html", title="TORCS_A3C", items=items)    

if __name__ == '__main__':
    app = tornado.web.Application([ 
        tornado.web.url(r'/', MyHandler),
        tornado.web.url(r'/upload', Upload) ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9090)
    print('Starting server on port 9090')
    tornado.ioloop.IOLoop.instance().start()