import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import datetime
import json
import os
import numpy as np

config=json.load(open("./torcs_central/config.json"))
resourcePath=config['resourcePath']

if not os.path.isdir(resourcePath):
    os.mkdir(resourcePath)
    print("Directory created at ",resourcePath)

global resource
resource=[]
log=[]
users = []
maxReward=250
def updateUsers():
    for log_ in log:
        user = log_[0]
        if user not in users:
            users.append(user)

print(os.getcwd())
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

class Download(tornado.web.RequestHandler):
    def get(self,key):
        if os.path.exists(os.path.join(resourcePath,'actor.h5')) and os.path.exists(os.path.join(resourcePath,'critic.h5')):
            filename = self.get_arguments('file',True)[0]
            if filename=='actor':
                with open(os.path.join(resourcePath,'actor.h5'),'rb') as fp:
                    fileData = fp.read()
                self.write(fileData)
            elif filename=='critic':
                with open(os.path.join(resourcePath,'actor.h5'),'rb') as fp:
                    fileData = fp.read()
                self.write(fileData)
            else:
                self.write(json.dumps({"actor":None,"critic":None}))
            # with open(os.path.join(resourcePath,'critic.h5')) as fp:
            #     criticData = fp.read()
            # self.write(json.dumps({"actor":open(os.path.join(resourcePath,'actor.h5')),"critic":open(os.path.join(resourcePath,'critic.h5'))}))
        else:
            self.write(json.dumps({"actor":None,"critic":None}))


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
        updateUsers()
        items=log
        self.render("template.html", title="TORCS_A3C", items=items, users=users,maxReward=maxReward)    

if __name__ == '__main__':
    settings = {
        "debug": True,
        "template_path": os.path.join(os.getcwd(),"torcs_central","templates"),
        "static_path": os.path.join(os.getcwd(),"torcs_central","templates","assets","css")
        }
    app = tornado.web.Application([ 
        tornado.web.url(r'/', MyHandler),
        tornado.web.url(r'/upload', Upload) ,
        tornado.web.url(r'/download/(.*)', Download) ],**settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9090)
    print('Starting server on port 9090')
    tornado.ioloop.IOLoop.instance().start()