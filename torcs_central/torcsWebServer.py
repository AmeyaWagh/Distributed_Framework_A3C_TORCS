import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import datetime

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

class MyHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        print(data)
        global resource
        resource.append(data)
        log.append([data['clientID'],data['cmd'],datetime.datetime.now().isoformat()])
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
    app = tornado.web.Application([ tornado.web.url(r'/', MyHandler) ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9090)
    print('Starting server on port 9090')
    tornado.ioloop.IOLoop.instance().start()